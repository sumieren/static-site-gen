from enum import Enum

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from inline_markdown_handler import text_to_textnodes

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
            case BlockType.HEADING:
                headers = ["#", "##", "###", "####", "#####", "######"]
                if any(block.startswith(header) for header in headers):
                    split = block.split(" ", 1)
                    value = len(split[0])

                    div.children.append(ParentNode(f"h{value}", text_to_children(split[1])))
            case BlockType.CODE:
                text = block[3:-3].lstrip()
                div.children.append(ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                clean_string = ""
                for line in lines:
                    # take out the >             
                    clean_string += line.replace(">", "").strip() + "\n"

                # take off the last newline
                clean_string = clean_string.strip()
                div.children.append(ParentNode("blockquote", text_to_children(clean_string)))
            case BlockType.U_LIST:
                div.children.append(ParentNode("ul", create_list_leaves(block)))
            case BlockType.O_LIST:
                div.children.append(ParentNode("ol", create_list_leaves(block)))
            case BlockType.PARAGRAPH:
                clean_text = block.replace("\n", " ")
                div.children.append(ParentNode("p", text_to_children(clean_text)))
            case _:
                raise Exception("Block not recognized")

    return div

def text_to_children(text):
    result = []

    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        result.append(text_node_to_html_node(node))

    return result

def create_list_leaves(text):
    leaves = []
    items = text.split("\n")

    for item in items:
        split = item.split(" ", 1)
        children = text_to_children(split[1])
        leaves.append(ParentNode("li", children))

    return leaves

def extract_title(markdown):
    split = markdown.split("\n")
    for line in split:
        if line.strip().startswith("# "):
            return line.replace("#", "").strip()
    raise Exception("no header found in markdown")