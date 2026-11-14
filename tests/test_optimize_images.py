import unittest
from pathlib import Path

from scripts.optimize_images import (
    ROOT,
    classify_loading,
    rewrite_html_text,
)


HEADER_PREFIX = (
    '<header class="site-header">'
    '<div class="container header-inner">'
    '<a href="index.html" class="brand">'
)
HEADER_SUFFIX = "</a></div></header>"
HERO_PREFIX = '<section class="hero"><div class="hero-visual">'
HERO_SUFFIX = "</div></section>"
BELOW_FOLD_PREFIX = (
    '<header class="site-header"></header>'
    '<main><section class="features"><div class="feature-card">'
)


class OptimizeImagesHtmlTests(unittest.TestCase):
    def test_wraps_webp_source_with_png_fallback(self):
        source = (
            f'{HEADER_PREFIX}'
            '<img src="images/logo.png" alt="WebHarvest" class="logo" />'
            f"{HEADER_SUFFIX}"
        )
        result = rewrite_html_text(source, ROOT / "about.html")
        self.assertIn(
            '<source type="image/webp" srcset="images/logo.webp" />',
            result,
        )
        self.assertIn(
            'src="images/logo.png"',
            result,
        )
        self.assertIn("<picture>", result)
        self.assertIn("</picture>", result)
        # PNG remains the img fallback; WebP is only a source.
        picture = result[
            result.index("<picture>") : result.index("</picture>") + 10
        ]
        self.assertLess(
            picture.index('type="image/webp"'),
            picture.index("<img "),
        )

    def test_preserves_alt_text_and_existing_class(self):
        source = (
            f"{HEADER_PREFIX}"
            '<img src="images/logo.png" alt="Keep this alt" '
            'class="logo brand-mark" data-role="brand" />'
            f"{HEADER_SUFFIX}"
        )
        result = rewrite_html_text(source, ROOT / "about.html")
        self.assertIn('alt="Keep this alt"', result)
        self.assertIn('class="logo brand-mark"', result)
        self.assertIn('data-role="brand"', result)
        self.assertIn('width="56"', result)
        self.assertIn('height="56"', result)

    def test_header_logo_and_hero_are_eager(self):
        header = (
            f"{HEADER_PREFIX}"
            '<img src="images/logo.png" alt="WebHarvest" class="logo" />'
            f"{HEADER_SUFFIX}"
        )
        hero = (
            f"{HERO_PREFIX}"
            '<img src="images/hero-icon.png" alt="Hero" />'
            f"{HERO_SUFFIX}"
        )
        header_result = rewrite_html_text(header, ROOT / "about.html")
        hero_result = rewrite_html_text(hero, ROOT / "about.html")
        self.assertIn('loading="eager"', header_result)
        self.assertIn('loading="eager"', hero_result)
        self.assertNotIn("fetchpriority", hero_result)

    def test_homepage_hero_gets_fetchpriority_high(self):
        hero = (
            f"{HERO_PREFIX}"
            '<img src="images/hero-icon.png" alt="Hero" />'
            f"{HERO_SUFFIX}"
        )
        result = rewrite_html_text(hero, ROOT / "index.html")
        self.assertIn('loading="eager"', result)
        self.assertIn('fetchpriority="high"', result)

    def test_below_the_fold_images_are_lazy(self):
        source = (
            f"{BELOW_FOLD_PREFIX}"
            '<img src="images/logo.png" alt="Inline logo" />'
            '<img src="images/hero-icon.png" alt="Inline hero" />'
            "</div></section></main>"
        )
        result = rewrite_html_text(source, ROOT / "about.html")
        self.assertEqual(result.count('loading="lazy"'), 2)
        self.assertNotIn('loading="eager"', result)
        self.assertNotIn("fetchpriority", result)

    def test_classify_loading_helpers(self):
        self.assertEqual(
            classify_loading(HEADER_PREFIX, "logo.png"),
            "eager",
        )
        self.assertEqual(
            classify_loading(HERO_PREFIX, "hero-icon.png"),
            "eager",
        )
        self.assertEqual(
            classify_loading(BELOW_FOLD_PREFIX, "logo.png"),
            "lazy",
        )
        self.assertEqual(
            classify_loading(HEADER_PREFIX, "hero-icon.png"),
            "lazy",
        )

    def test_rewrite_is_idempotent(self):
        source = (
            f"{HEADER_PREFIX}"
            '<img src="images/logo.png" alt="WebHarvest" class="logo" />'
            f"{HEADER_SUFFIX}"
            f"{HERO_PREFIX}"
            '<img src="images/hero-icon.png" alt="Hero" />'
            f"{HERO_SUFFIX}"
            f"{BELOW_FOLD_PREFIX}"
            '<img src="images/logo.png" alt="Later" />'
            "</div></section></main>"
        )
        page = Path("about.html")
        once = rewrite_html_text(source, page)
        twice = rewrite_html_text(once, page)
        self.assertEqual(once, twice)
        self.assertEqual(once.count("<picture>"), 3)
        self.assertEqual(once.count('loading="eager"'), 2)
        self.assertEqual(once.count('loading="lazy"'), 1)


if __name__ == "__main__":
    unittest.main()
