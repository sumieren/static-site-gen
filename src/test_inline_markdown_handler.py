import unittest

from textnode import TextNode, TextType
from inline_markdown_handler import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    
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
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev) or [two](https://www.boot.dev/two)"
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
            "This is text with a [link]()"
        )
        self.assertListEqual([("link", "")], matches)

    def test_extract_markdown_link_on_image(self):
        matches = extract_markdown_links(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
        

    # split to image or link node tests
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
                [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
                ], new_nodes)
        
    def test_split_image_trailing(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) with trailing text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
                [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" with trailing text", TextType.TEXT)
                ], new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_same_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and the same ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and the same ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )


    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
                [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
                ], new_nodes)
        
    def test_split_link_trailing(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) with trailing text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
                [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" with trailing text", TextType.TEXT)
                ], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.boot.dev/two)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev/two"
                ),
            ],
            new_nodes,
        )

    def test_split_same_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and the same [link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and the same ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes,
        )

    def test_no_images_found(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_type(self):
        node = TextNode("This won't be processed", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_non_text_node_link(self):
        node = TextNode("This won't be processed even with a [link](https://www.boot.dev)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_multiple_links(self):
        nodes = [
            TextNode(
            "This is text with a [link](https://www.boot.dev)",
            TextType.TEXT),
            TextNode(
            "This is another text with a [link](https://www.boot.dev)",
            TextType.TEXT),
            TextNode(
            "This is yet another text with a [link](https://www.boot.dev)",
            TextType.TEXT),
            ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
                [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is another text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("This is yet another text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev")
                ], new_nodes)
        
    # test for the final conversion
    def test_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
                [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ], nodes)
        

if __name__ == "__main__":
    unittest.main()