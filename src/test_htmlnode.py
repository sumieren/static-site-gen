import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


    # LeafNode tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "www.website.com", {"href": "www.website.com"})
        self.assertEqual(node.to_html(), '<a href="www.website.com">www.website.com</a>')

    def test_leaf_child(self):
        node = LeafNode("p", "Hello, world!")
        self.assertIsNone(node.children)

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual("Hello, world!", node.to_html())

    def test_leaf_no_value(self):
        node = LeafNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", "child3")
        child_node4 = LeafNode("span", "child4")
        child_node5 = LeafNode("span", "child5")
        parent_node3 = ParentNode("div", [child_node5])
        parent_node2 = ParentNode("div", [child_node4])
        parent_node1 = ParentNode("div", [child_node2, child_node3, parent_node2])
        parent_node = ParentNode("div", [child_node, child_node1, parent_node1, parent_node3])
        
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child1</span><div><span>child2</span><span>child3</span><div><span>child4</span></div></div><div><span>child5</span></div></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()


    # ParentNode tests
    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_list(self):
        parent_node = ParentNode("div", [])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "website.com", {"href": "https://www.website.com", "target": "_blank"})
        child_node1 = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, child_node1])

        self.assertEqual(parent_node.to_html(), '<div><a href="https://www.website.com" target="_blank">website.com</a><span>child</span></div>')

if __name__ == "__main__":
    unittest.main()