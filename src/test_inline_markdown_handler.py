import unittest

from textnode import TextNode, TextType
from inline_markdown_handler import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestDelimiter(unittest.TestCase):
    def test_bold(self):
        nodes = [TextNode("This is a **test** case", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [TextNode("This is a ", TextType.TEXT, None), TextNode("test", TextType.BOLD, None), TextNode(" case", TextType.TEXT, None)])

    def test_multiple_bold(self):
        nodes = [TextNode("This is a **test** case with **more** bold", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [TextNode("This is a ", TextType.TEXT, None), TextNode("test", TextType.BOLD, None), TextNode(" case with ", TextType.TEXT, None), TextNode("more", TextType.BOLD, None), TextNode(" bold", TextType.TEXT, None)])

    def test_bold_node(self):
        nodes = [TextNode("test", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [TextNode("test", TextType.BOLD, None)])

    def test_not_bold_node(self):
        nodes = [TextNode("test", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [TextNode("test", TextType.TEXT, None)])

    def test_nested(self):
        nodes = [TextNode("This is a **test _case `with` nested_ inline**", TextType.TEXT)]
        step = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        step2 = split_nodes_delimiter(step, "_", TextType.ITALIC)
        self.assertEqual(split_nodes_delimiter(step2, "`", TextType.CODE), [TextNode("This is a ", TextType.TEXT, None), TextNode("test _case `with` nested_ inline", TextType.BOLD, None)])

    
    # regex tests
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) or ![two](https://i.imgur.com/zjjcJKZ.jpg)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("two", "https://i.imgur.com/zjjcJKZ.jpg")], matches)
        
    def test_extract_markdown_image_whitespace(self):
        matches = extract_markdown_images(
            "This is text with an ![image and long alt text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image and long alt text", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_no_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_wrong(self):
        matches = extract_markdown_images(
            "This is text with an !(image and long alt text)[https://i.imgur.com/zjjcJKZ.png]"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_no_image(self):
        matches = extract_markdown_images(
            "This is text with an ![]()"
        )
        self.assertListEqual([("", "")], matches)

    def test_extract_markdown_image_no_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image]()"
        )
        self.assertListEqual([("image", "")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev) or [two](https://www.boot.dev/two)"
        )
        self.assertListEqual([("link", "https://www.boot.dev"), ("two", "https://www.boot.dev/two")], matches)

    def test_extract_markdown_link_whitespace(self):
        matches = extract_markdown_links(
            "This is text with an [link and long text](https://www.boot.dev)"
        )
        self.assertListEqual([("link and long text", "https://www.boot.dev")], matches)

    def test_extract_markdown_link_no_text(self):
        matches = extract_markdown_links(
            "This is text with an [](https://www.boot.dev)"
        )
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_link_wrong(self):
        matches = extract_markdown_links(
            "This is text with an (link)[https://www.boot.dev]"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_no_link(self):
        matches = extract_markdown_links(
            "This is text with an []()"
        )
        self.assertListEqual([("", "")], matches)

    def test_extract_markdown_link_no_url(self):
        matches = extract_markdown_links(
            "This is text with an [link]()"
        )
        self.assertListEqual([("link", "")], matches)

    def test_extract_markdown_link_on_image(self):
        matches = extract_markdown_links(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
        