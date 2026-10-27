"""Markdown-to-page checks for utils/md_to_artefatto.py.

Run with: poetry run python -m unittest discover -s tests -v
"""

import unittest

from utils.md_to_artefatto import render_body


class RenderBodyTest(unittest.TestCase):
    def test_table_without_outer_pipes_becomes_html_table(self):
        _, body = render_body("## Tabella\n\nNF | TP\n---|---\nUDR | `3 / 6`\n")
        self.assertIn('<section id="tabella">', body)
        self.assertIn("<th>NF</th><th>TP</th>", body)
        self.assertIn("<td>UDR</td><td><code>3 / 6</code></td>", body)

    def test_markup_inside_code_is_escaped_not_interpreted(self):
        _, body = render_body("Run `**x** <b>` e **grassetto**.\n")
        self.assertIn("<code>**x** &lt;b&gt;</code>", body)
        self.assertIn("<strong>grassetto</strong>", body)

    def test_h1_is_returned_and_sections_are_closed(self):
        h1, body = render_body("# Titolo\n\n## Uno\n\ntesto\n\n## Uno\n\naltro\n")
        self.assertEqual(h1, "Titolo")
        self.assertEqual(body.count("<section"), 2)
        self.assertEqual(body.count("</section>"), 2)
        self.assertIn('id="uno-2"', body)


if __name__ == "__main__":
    unittest.main()
