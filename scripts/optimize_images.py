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
- ``loading="eager"`` is used only for header logos and hero imagery;
  other placements use ``loading="lazy"``. ``fetchpriority="high"`` is
  reserved for the homepage hero.

The transferred 1024px originals remain in the Git history of the transfer
commit. Re-running this script on the already resized fallbacks keeps the
target dimensions and rewrites the WebP files. Pass ``--html-only`` to
rewrite markup without touching image binaries.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

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
HERO_VISUAL_OPEN_RE = re.compile(
    r"<div\b[^>]*\bclass=\"[^\"]*\bhero-visual\b[^\"]*\"[^>]*>",
    re.IGNORECASE,
)
DIV_TAG_RE = re.compile(r"</?div\b[^>]*>", re.IGNORECASE)


def require_webp() -> None:
    try:
        from PIL import features
    except ImportError as exc:  # pragma: no cover - environment dependency
        sys.exit(f"Pillow is required to encode images: {exc}")
    if not features.check("webp"):
        sys.exit("Pillow was built without WebP support")


def resize_to(image, target: int):
    from PIL import Image

    if image.width == target and image.height == target:
        return image
    if image.width < target or image.height < target:
        sys.exit(f"refusing to upscale {image.size} to {target}")
    if image.width != image.height:
        sys.exit(f"expected a square image, got {image.size}")
    return image.resize((target, target), Image.Resampling.LANCZOS)


def optimize_file(name: str) -> None:
    from PIL import Image

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


def is_in_header(preceding_html: str) -> bool:
    return preceding_html.rfind("<header") > preceding_html.rfind("</header")


def is_in_hero_visual(preceding_html: str) -> bool:
    matches = list(HERO_VISUAL_OPEN_RE.finditer(preceding_html))
    if not matches:
        return False
    after = preceding_html[matches[-1].end() :]
    depth = 1
    for match in DIV_TAG_RE.finditer(after):
        if match.group(0).lower().startswith("</"):
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            return False
    return depth > 0


def classify_loading(preceding_html: str, filename: str) -> str:
    """Return eager only for header logos and hero-visual imagery."""
    if filename in {"logo.png", "logo-white-bg.png"} and is_in_header(
        preceding_html
    ):
        return "eager"
    if filename == "hero-icon.png" and is_in_hero_visual(preceding_html):
        return "eager"
    return "lazy"


def build_img_tag(
    tag: str, src: str, page: Path, preceding_html: str
) -> str:
    attrs = dict(ATTR_RE.findall(tag))
    filename = src.rsplit("/", 1)[-1]
    width, height = DISPLAY_SIZE[filename]
    attrs["src"] = src
    attrs["width"] = str(width)
    attrs["height"] = str(height)
    attrs["loading"] = classify_loading(preceding_html, filename)
    if (
        attrs["loading"] == "eager"
        and filename == "hero-icon.png"
        and page.name == "index.html"
        and page.parent == ROOT
    ):
        attrs["fetchpriority"] = "high"
    else:
        attrs.pop("fetchpriority", None)
    ordered = ["src", "alt", "class", "width", "height", "loading", "fetchpriority"]
    parts = []
    for key in ordered:
        if key in attrs:
            parts.append(f'{key}="{attrs.pop(key)}"')
    for key, value in attrs.items():
        parts.append(f'{key}="{value}"')
    return "<img " + " ".join(parts) + " />"


def wrap_picture(img_tag: str, src: str) -> str:
    webp = re.sub(r"\.png$", ".webp", src, flags=re.IGNORECASE)
    return (
        "<picture>\n"
        f'                    <source type="image/webp" srcset="{webp}" />\n'
        f"                    {img_tag}\n"
        "                </picture>"
    )


def picture_for(tag: str, src: str, page: Path, preceding_html: str) -> str:
    return wrap_picture(build_img_tag(tag, src, page, preceding_html), src)


def rewrite_html_text(original: str, page: Path) -> str:
    """Rewrite optimized-image markup. Pure: does not touch the filesystem."""
    pieces: list[str] = []
    cursor = 0
    for match in IMG_RE.finditer(original):
        preceding = original[: match.start()]
        img_tag = build_img_tag(
            match.group(0), match.group("src"), page, preceding
        )
        if already_in_picture(original, match.start()):
            replacement = img_tag
        else:
            replacement = wrap_picture(img_tag, match.group("src"))
        pieces.append(original[cursor : match.start()])
        pieces.append(replacement)
        cursor = match.end()
    if not pieces:
        return original
    pieces.append(original[cursor:])
    return "".join(pieces)


def rewrite_html(page: Path) -> bool:
    original = page.read_text(encoding="utf-8")
    updated = rewrite_html_text(original, page)
    if updated == original:
        return False
    page.write_text(updated, encoding="utf-8")
    return True


def rewrite_all_html(root: Path = ROOT) -> int:
    updated = 0
    for page in sorted(root.rglob("*.html")):
        if rewrite_html(page):
            updated += 1
    return updated


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="Rewrite HTML picture markup without re-encoding image files",
    )
    args = parser.parse_args(argv)

    if not args.html_only:
        require_webp()
        for name in TARGETS:
            optimize_file(name)
        image_count = len(TARGETS)
    else:
        image_count = 0

    updated = rewrite_all_html(ROOT)
    print(
        f"optimized {image_count} images; updated {updated} HTML files"
    )


if __name__ == "__main__":
    main()
