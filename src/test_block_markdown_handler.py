import unittest

from block_markdown_handler import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

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

if __name__ == "__main__":
    unittest.main()