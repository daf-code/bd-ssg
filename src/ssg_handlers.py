from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType

#TextNode to HTMLNode
def textnode_to_htmlnode(textnode: TextNode) -> HTMLNode:
# It should handle each type of the TextType enum. If it gets a TextNode that is none of those types, it should raise an exception.
    # TextType.TEXT: This should become a LeafNode with no tag, just a raw text value.
    # TextType.BOLD: This should become a LeafNode with a “b” tag and the text
    # TextType.ITALIC: “i” tag, text
    # TextType.CODE: “code” tag, text
    # TextType.LINK: “a” tag, anchor text, and “href” prop
    # TextType.IMAGE: “img” tag, empty string value, “src” and “alt” props (“src” is the image URL, “alt” is the alt text)
    valid_types = [TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE]
    
    if textnode.text_type not in valid_types:
        raise ValueError(f"Invalid text type: {textnode.text_type}")
    
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text}) 
   