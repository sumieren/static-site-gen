from textnode import TextType

# An HTMLNode without a tag will just render as raw text
# An HTMLNode without a value will be assumed to have children
# An HTMLNode without children will be assumed to have a value
# An HTMLNode without props simply won't have any attributes
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("function not implemented in child class")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for attribute in self.props:
            result += f' {attribute}="{self.props[attribute]}"'
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if (self.value == None):
            raise ValueError("leaf node must have a value")

        if (self.tag == None):
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if (self.tag == None):
            raise ValueError("parent node must have a tag")
        if (self.children == None or self.children == []):
            raise ValueError("parent node must have at least 1 child")
        
        result = ""

        for child in self.children:
            result += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
    
def text_node_to_html_node(node):
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {'href': f"{node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", { 'src': f"{node.url}", 'alt': f"{node.text}" })
        case _:
            raise Exception("node type not recognized")
