import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.generate_sitemap import SITEMAP_NS, generate_sitemap


class GenerateSitemapTests(unittest.TestCase):
    def test_generates_html_and_xml_example_urls(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text("<html></html>", encoding="utf-8")
            (root / "documentation").mkdir()
            (root / "documentation" / "guide.html").write_text(
                "<html></html>", encoding="utf-8"
            )
            (root / "examples").mkdir()
            (root / "examples" / "sample.xml").write_text(
                "<config />", encoding="utf-8"
            )
            (root / "internal.xml").write_text(
                "<internal />", encoding="utf-8"
            )
            output = root / "sitemap.xml"

            count = generate_sitemap(root, "https://example.test", output)

            document = ET.parse(output)
            locations = [
                node.text
                for node in document.findall(
                    f".//{{{SITEMAP_NS}}}loc"
                )
            ]
            self.assertEqual(count, 3)
            self.assertEqual(
                locations,
                [
                    "https://example.test/documentation/guide.html",
                    "https://example.test/examples/sample.xml",
                    "https://example.test/index.html",
                ],
            )
            self.assertEqual(
                document.findall(f".//{{{SITEMAP_NS}}}lastmod"),
                [],
            )

    def test_omits_lastmod_for_reproducible_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.html").write_text("<html></html>", encoding="utf-8")
            output = root / "sitemap.xml"

            generate_sitemap(root, "https://example.test", output)
            first = output.read_bytes()
            generate_sitemap(root, "https://example.test", output)
            second = output.read_bytes()

            self.assertEqual(first, second)
            self.assertNotIn(b"lastmod", first)

    def test_rejects_non_http_base_url(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with self.assertRaises(ValueError):
                generate_sitemap(root, "file:///tmp/site", root / "sitemap.xml")


if __name__ == "__main__":
    unittest.main()
