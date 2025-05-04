import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        
        else:
            split = node.text.split(delimiter)
            
            if (len(split) % 2) == 0:
                raise Exception(f"Node {node} contains invalid Markdown syntax")

            for i in range(0, len(split)):             
                if split[i]:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split[i], TextType.TEXT))
                    elif i % 2 == 1:
                        new_nodes.append(TextNode(split[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)", text)