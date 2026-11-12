#!/usr/bin/env python3
"""Generate a sitemap for the standalone WebHarvest website.

The canonical base URL is deliberately explicit: pass --base-url or set
WEBSITE_BASE_URL. This prevents accidentally publishing a sitemap for the
legacy hosting domain after the site has moved.

``lastmod`` is omitted on purpose. Filesystem modification times are not
stable across clean checkouts or build agents, and inventing timestamps
would be misleading. The sitemap protocol treats ``lastmod`` as optional.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from urllib.parse import quote
import xml.etree.ElementTree as ET

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", SITEMAP_NS)


def discover_pages(site_root: Path) -> list[Path]:
    """Return public HTML pages and downloadable XML examples."""
    pages = set(site_root.rglob("*.html"))
    examples = site_root / "examples"
    if examples.is_dir():
        pages.update(examples.rglob("*.xml"))
    return sorted(
        (path for path in pages if path.is_file()),
        key=lambda path: path.relative_to(site_root).as_posix(),
    )


def generate_sitemap(site_root: Path, base_url: str, output: Path) -> int:
    """Write a sitemap and return the number of URLs written."""
    if not base_url.startswith(("https://", "http://")):
        raise ValueError("base_url must be an absolute HTTP(S) URL")

    root = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    base = base_url.rstrip("/") + "/"

    for page in discover_pages(site_root):
        relative = page.relative_to(site_root).as_posix()
        url = ET.SubElement(root, f"{{{SITEMAP_NS}}}url")
        loc = ET.SubElement(url, f"{{{SITEMAP_NS}}}loc")
        loc.text = base + quote(relative, safe="/:@")

    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(
        output, encoding="utf-8", xml_declaration=True
    )
    return len(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default=os.environ.get("WEBSITE_BASE_URL"),
        help="Canonical site URL (or set WEBSITE_BASE_URL)",
    )
    parser.add_argument(
        "--site-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Website root directory (default: repository root)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Sitemap output path (default: <site-root>/sitemap.xml)",
    )
    args = parser.parse_args()

    if not args.base_url:
        parser.error("provide --base-url or set WEBSITE_BASE_URL")

    output = args.output or args.site_root / "sitemap.xml"
    count = generate_sitemap(args.site_root, args.base_url, output)
    print(f"Generated {count} URLs in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
