#!/usr/bin/env python3
"""Create display-sized PNG fallbacks and lossless WebP variants.

Prerequisites
-------------
Python 3 and Pillow built with WebP support (verified with Pillow 13):

    python3 -m pip install Pillow
    python3 -c "from PIL import features; assert features.check('webp')"

The script does not add a runtime dependency to the website. AVIF is not
emitted: the local avifenc 1.4.1 encoder is available, but lossy encodes
changed the alpha channel and lossless AVIF was larger than lossless WebP.

Parameters (deterministic)
--------------------------
- Logo assets are resized to 168x168 (3x the 56px header slot). ``logo.png``
  and ``logo-white-bg.png`` are different images and are never substituted.
- ``hero-icon.png`` is resized to 640x640 (2x the 320px max-width).
- Resampling is Lanczos. Images are never upscaled.
- PNG fallback: compress level 9, optimize=True, original color mode kept.
- WebP: lossless, quality 100, method 6.
- HTML ``<img>`` tags for these three files are wrapped in ``<picture>``
  with a WebP source and the PNG fallback. Re-running is idempotent.

The transferred 1024px originals remain in the Git history of the transfer
commit. Re-running this script on the already resized fallbacks keeps the
target dimensions and rewrites the WebP files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, features

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"

LOGO_TARGET = 168
HERO_TARGET = 640
TARGETS = {
    "logo.png": LOGO_TARGET,
    "logo-white-bg.png": LOGO_TARGET,
    "hero-icon.png": HERO_TARGET,
}
DISPLAY_SIZE = {
    "logo.png": (56, 56),
    "logo-white-bg.png": (56, 56),
    "hero-icon.png": (320, 320),
}

IMG_RE = re.compile(
    r"<img\b[^>]*\bsrc=\"(?P<src>[^\"]*/(?:hero-icon|logo-white-bg|logo)\.png)\"[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
ATTR_RE = re.compile(r"([:\w-]+)\s*=\s*\"([^\"]*)\"")


def require_webp() -> None:
    if not features.check("webp"):
        sys.exit("Pillow was built without WebP support")


def resize_to(image: Image.Image, target: int) -> Image.Image:
    if image.width == target and image.height == target:
        return image
    if image.width < target or image.height < target:
        sys.exit(f"refusing to upscale {image.size} to {target}")
    if image.width != image.height:
        sys.exit(f"expected a square image, got {image.size}")
    return image.resize((target, target), Image.Resampling.LANCZOS)


def optimize_file(name: str) -> None:
    source = IMAGE_DIR / name
    with Image.open(source) as image:
        image.load()
        mode = image.mode
        resized = resize_to(image, TARGETS[name])
        if resized.mode != mode:
            resized = resized.convert(mode)
        resized.save(source, "PNG", optimize=True, compress_level=9)
        webp = source.with_suffix(".webp")
        resized.save(webp, "WEBP", lossless=True, quality=100, method=6)


def already_in_picture(text: str, start: int) -> bool:
    before = text[:start]
    return before.rfind("<picture") > before.rfind("</picture>")


def picture_for(tag: str, src: str, page: Path) -> str:
    attrs = dict(ATTR_RE.findall(tag))
    filename = src.rsplit("/", 1)[-1]
    width, height = DISPLAY_SIZE[filename]
    attrs["width"] = str(width)
    attrs["height"] = str(height)
    attrs["loading"] = "eager"
    if filename == "hero-icon.png" and page.name == "index.html" and page.parent == ROOT:
        attrs["fetchpriority"] = "high"
    ordered = ["src", "alt", "class", "width", "height", "loading", "fetchpriority"]
    parts = []
    for key in ordered:
        if key in attrs:
            parts.append(f'{key}="{attrs.pop(key)}"')
    for key, value in attrs.items():
        parts.append(f'{key}="{value}"')
    img = "<img " + " ".join(parts) + " />"
    webp = re.sub(r"\.png$", ".webp", src, flags=re.IGNORECASE)
    return (
        "<picture>\n"
        f'                    <source type="image/webp" srcset="{webp}" />\n'
        f"                    {img}\n"
        "                </picture>"
    )


def rewrite_html(page: Path) -> bool:
    original = page.read_text(encoding="utf-8")
    pieces = []
    cursor = 0
    changed = False
    for match in IMG_RE.finditer(original):
        if already_in_picture(original, match.start()):
            continue
        pieces.append(original[cursor:match.start()])
        pieces.append(picture_for(match.group(0), match.group("src"), page))
        cursor = match.end()
        changed = True
    if not changed:
        return False
    pieces.append(original[cursor:])
    page.write_text("".join(pieces), encoding="utf-8")
    return True


def main() -> None:
    require_webp()
    for name in TARGETS:
        optimize_file(name)
    updated = 0
    for page in ROOT.rglob("*.html"):
        if rewrite_html(page):
            updated += 1
    print(f"optimized {len(TARGETS)} images; updated {updated} HTML files")


if __name__ == "__main__":
    main()
