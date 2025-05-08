from enum import Enum

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ordered_list"



def markdown_to_blocks(markdown):
    blocks = []
    split = markdown.split("\n\n")

    # treat each block
    for block in split:
        # take out any leading/trailing whitespaces and newlines
        new_block = block.strip()

        # split each block into lines and strip those
        lines = new_block.split("\n")
        rejoin = []
        for line in lines:
            rejoin.append(line.strip())
        new_block = "\n".join(rejoin)

        # if the block isn't empty, append it
        if new_block:
            blocks.append(new_block)

    return blocks

def block_to_block_type(block):
    split = block.split(" ")
    lines = block.split("\n")
    # check if is header
    headers = ["#", "##", "###", "####", "#####", "######"]
    if split[0] in headers:
        # if there is any text after
        if len(split) > 1:
            return BlockType.HEADING

    # check if is code
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    # check if is quote
    if all(line.split(" ")[0] == ">" for line in lines):
        return BlockType.QUOTE
    
    # check if is unordered list
    if all(line.split(" ")[0] == "-" for line in lines):
        return BlockType.U_LIST
    
    ordered_list = True
    # check if is ordered list
    for i in range(0, len(lines)):
        start = lines[i].split(" ")[0]
        if start != f"{i+1}.":
            ordered_list = False

    if ordered_list:
        return BlockType.O_LIST
    
    # else 
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    div = ParentNode("div", [])

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.CODE:
                text = block[3:-3].lstrip()
                div.children.append(ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))]))
            case _:
                raise Exception("Block not recognized")

    return div
