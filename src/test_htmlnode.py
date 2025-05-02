import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is text within a tag", [HTMLNode("br"), HTMLNode("b")])
        self.assertEqual('HTMLNode(p, This is text within a tag, [HTMLNode(br, None, None, None), HTMLNode(b, None, None, None)], None)', repr(node))

    def test_values(self):
        node = HTMLNode("div", "This is text within a tag")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "This is text within a tag")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_to_html(self):
        node = HTMLNode("p", "This is text within a tag", [HTMLNode("br"), HTMLNode("b")])
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("a", "website.com", None, {"href": "https://www.website.com", "target": "_blank"})
        self.assertEqual(' href="https://www.website.com" target="_blank"', node.props_to_html())

if __name__ == "__main__":
    unittest.main()