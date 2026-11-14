#!/usr/bin/env python3
"""One-time repair helper for XML examples embedded in website HTML.

This is intentionally scoped to the four pages previously targeted by the
application-repository helper. It does not traverse or rewrite the whole site.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

TARGETS = (
    Path("documentation/css-selectors-guide.html"),
    Path("documentation/file-advanced-patterns.html"),
    Path("documentation/rate-limiting-guide.html"),
    Path("documentation/tutorial-form-submit-pagination.html"),
)
CODE_BLOCK = re.compile(
    r'(<pre><code class="language-xml">)(.*?)(</code></pre>)',
    re.DOTALL,
)
WEBHARVEST_TAGS = (
    "&lt;def", "&lt;http", "&lt;xpath", "&lt;xquery",
    "&lt;loop", "&lt;file",
)


def repair_content(content: str) -> str:
    """Add a config wrapper to unwrapped WebHarvest XML code samples."""
    def replace(match: re.Match[str]) -> str:
        body = match.group(2)
        if "&lt;config" in body or "&lt;?xml version" in body:
            return match.group(0)
        if not any(tag in body for tag in WEBHARVEST_TAGS):
            return match.group(0)
        wrapped = (
            '&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n'
            '&lt;config xmlns="http://org.webharvest/schema/2.1/core"&gt;\n'
            f'{body.strip()}\n'
            '&lt;/config&gt;'
        )
        return f"{match.group(1)}{wrapped}{match.group(3)}"

    return CODE_BLOCK.sub(replace, content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Website root directory (default: repository root)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report pages that need repair without writing changes",
    )
    args = parser.parse_args()

    changed = 0
    for relative in TARGETS:
        page = args.site_root / relative
        if not page.is_file():
            print(f"SKIP missing: {relative}")
            continue
        original = page.read_text(encoding="utf-8")
        repaired = repair_content(original)
        if repaired == original:
            print(f"OK: {relative}")
            continue
        changed += 1
        if args.check:
            print(f"NEEDS REPAIR: {relative}")
        else:
            page.write_text(repaired, encoding="utf-8")
            print(f"REPAIRED: {relative}")

    print(f"{changed} page(s) {'need repair' if args.check else 'repaired'}")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
