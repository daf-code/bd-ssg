import unittest
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from ssg_handlers import textnode_to_htmlnode


class TestTextNode(unittest.TestCase):
    
    def test_tn_to_html_normal(self):
        tnode = TextNode("This is a NORMAL text node", TextType.NORMAL)
        hnode = textnode_to_htmlnode(tnode)
        self.assertEqual(hnode, LeafNode(None, "This is a NORMAL text node"))   
    
    def test_tn_to_html_bold(self):
        tnode = TextNode("This is a BOLD text node", TextType.BOLD)
        hnode = textnode_to_htmlnode(tnode)
        self.assertEqual(hnode, LeafNode("b", "This is a BOLD text node"))
    
    def test_tn_to_html_italic(self):
        tnode = TextNode("This is a ITALIC text node", TextType.ITALIC)
        hnode = textnode_to_htmlnode(tnode)
        self.assertEqual(hnode, LeafNode("i", "This is a ITALIC text node"))

    def test_tn_to_html_code(self):
        tnode = TextNode("This is a CODE text node", TextType.CODE)
        hnode = textnode_to_htmlnode(tnode)
        self.assertEqual(hnode, LeafNode("code", "This is a CODE text node"))
    
    def test_tn_to_html_link(self):
        tnode = TextNode("This is a LINK text node", TextType.LINK, "https://www.boot.dev")
        hnode = textnode_to_htmlnode(tnode)
        self.assertEqual(hnode, LeafNode("a", "This is a LINK text node", {"href": "https://www.boot.dev"}))    
        
    def test_tn_to_html_image(self):
        tnode = TextNode("This is a IMAGE text node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        hnode = textnode_to_htmlnode(tnode)
        self.assertEqual(hnode, LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp", "alt": "This is a IMAGE text node"}))
            
    def test_tn_to_html_invalid_type(self):
        tnode = TextNode("This is a INVALID text node", TextType.INVALID)
        with self.assertRaises(ValueError):
            textnode_to_htmlnode(tnode)
