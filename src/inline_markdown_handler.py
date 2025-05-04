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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:     
        # First check if this is even a TEXT node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # Preserve non-TEXT nodes as-is
            continue

        text = node.text
        images = extract_markdown_images(node.text)

        # check if there are any images, else node is just text
        if not images:
            new_nodes.append(node)
            continue

        else:
            # get list of delimiters in string
            delimiters = []
            for image in images:
                delimiters.append(f"![{image[0]}]({image[1]})")

            # use i to track where we are in images, since we know images length = delimiters length
            i = 0
            for delimiter in delimiters:
                # split text based on first delimiter, add as text and image nodes. 
                # Then overwrite text with the rest of the string so we don't split anything we've already added.
                # don't forget to increment i
                split = text.split(delimiter, 1)
                new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                text = split[1]
                i += 1
            
            # at the end, append any leftover text if it exists
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # First check if this is even a TEXT node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # Preserve non-TEXT nodes as-is
            continue

        text = node.text
        links = extract_markdown_links(node.text)

        # check if there are any links, else node is just text
        if not links:
            new_nodes.append(node)
            continue

        else:
            # get list of delimiters in string
            delimiters = []
            for link in links:
                delimiters.append(f"[{link[0]}]({link[1]})")

            # use i to track where we are in images, since we know images length = delimiters length
            i = 0
            for delimiter in delimiters:
                # split text based on first delimiter, add as text and image nodes. 
                # Then overwrite text with the rest of the string so we don't split anything we've already added.
                # don't forget to increment i
                split = text.split(delimiter, 1)
                new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                text = split[1]
                i += 1
            
            # at the end, append any leftover text if it exists
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    # append returned nodes one by one
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes