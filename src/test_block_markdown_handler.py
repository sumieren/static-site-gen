import unittest

from block_markdown_handler import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title

class TestBlockHandler(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_trailing_whitespace(self):
        md = """

    This is **bolded** paragraph


    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line




    - This is a list
    - with items


    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_empty(self):
        md = """
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
            ],
        )

    def test_markdown_single(self):
        md = """



    This is **bolded** paragraph

    


    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )

    def test_block_heading(self):
        blocks = ["# Heading", "## Heading", "### Heading", "#### Heading", "##### Heading", "###### Heading"] 
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_heading_wrong(self):
        blocks = ["#Heading", "######## Heading", "##"]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_code(self):
        blocks = ["``` code ```", "```longer code block```", "```code\nblock\nwith\nnewlines```"] 
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_code_wrong(self):
        blocks = ["``code``", "`code`", "```code``"]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_quote(self):
        blocks = ["> this\n> is \n> a\n> quote", "> basic quote", "> this > is a single > a quote", "> this is a \n> multi line > quote"] 
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_quote_wrong(self):
        blocks = ["> this\n isn't", "> every line\n> needs to have\n the same starter"]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
            
    def test_block_ulist(self):
        blocks = ["- this\n- is \n- a\n- ulist", "- basic ulist", "- this - is a single - a ulist", "- this is a \n- multi line - ulist"] 
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.U_LIST)
    
    def test_block_ulist_wrong(self):
        blocks = ["- this\n isn't", "- every line\n- needs to have\n the same starter"]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_olist(self):
        blocks = ["1. this is a list", "1. this is a\n2. List with three\n3. entries", "1. This is a 2. list with\n2. Two entries 4. not four."] 
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.O_LIST)
    
    def test_block_olist_wrong(self):
        blocks = ["1. this list is \n3. incorrectly ordered", "1. this one\n is missing numbering"]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # test markdown to html block
    def test_header(self):
        md = """
            #### test
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>test</h4></div>",
        )

    def test_quote(self):
        md = """
            > this is a long block, it is quite long
            > and it has multiple lines, isn't that crazy?
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a long block, it is quite long\nand it has multiple lines, isn't that crazy?</blockquote></div>",
        )

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_ulist(self):
        md = """
            - This is a list
            - it has 4 items
            - this is the third
            - now the list is done

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>it has 4 items</li><li>this is the third</li><li>now the list is done</li></ul></div>",
        )

    def test_olist(self):
        md = """
            1. This is a list 
            2. it is ordered
            3. this is the third
            4. now the list is done

            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is a list</li><li>it is ordered</li><li>this is the third</li><li>now the list is done</li></ol></div>",
        )

    def test_title(self):
        md = """
            # Title here

            This is the body.

            """
        title = extract_title(md)
        self.assertEqual(title, "Title here")

    def test_title_wrong(self):
        md = """
            ### No title here

            ## This isn't a title

            #Neither is this

            This is the body.

            """
        with self.assertRaises(Exception):
            title = extract_title(md)

    def test_title_order(self):
        md = """
            Text first

            ### Then some other stuff

            ## Or this kind of stuff

            # But this is the title

            """
        title = extract_title(md)
        self.assertEqual(title, "But this is the title")

if __name__ == "__main__":
    unittest.main()