import unittest

from scripts.fix_html_examples import repair_content


class FixHtmlExamplesTests(unittest.TestCase):
    def test_wraps_unwrapped_webharvest_xml_example(self):
        source = (
            '<pre><code class="language-xml">'
            '&lt;http&gt;https://example.test&lt;/http&gt;'
            '</code></pre>'
        )
        result = repair_content(source)
        self.assertIn("&lt;config", result)
        self.assertIn("&lt;/config&gt;", result)

    def test_leaves_already_wrapped_example_unchanged(self):
        source = (
            '<pre><code class="language-xml">'
            '&lt;config&gt;&lt;http /&gt;&lt;/config&gt;'
            '</code></pre>'
        )
        self.assertEqual(repair_content(source), source)

    def test_repair_is_idempotent(self):
        source = (
            '<pre><code class="language-xml">'
            '&lt;http&gt;https://example.test&lt;/http&gt;'
            '</code></pre>'
        )
        once = repair_content(source)
        self.assertEqual(repair_content(once), once)

    def test_leaves_non_webharvest_xml_unchanged(self):
        source = '<pre><code class="language-xml">&lt;root /&gt;</code></pre>'
        self.assertEqual(repair_content(source), source)


if __name__ == "__main__":
    unittest.main()
