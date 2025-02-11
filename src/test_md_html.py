import unittest
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from md_to_html import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node_empty_1(self):
        """Test empty markdown input"""
        node = markdown_to_html_node("")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, [])

    def test_markdown_to_html_node_single_paragraph_2(self):
        """Test basic paragraph conversion"""
        node = markdown_to_html_node("This is a paragraph")
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].to_html(), "<p>This is a paragraph</p>")

    def test_markdown_to_html_node_header_3(self):
        """Test header conversion"""
        node = markdown_to_html_node("# Heading 1")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[0].to_html(), "<h1>Heading 1</h1>")

    def test_markdown_to_html_node_unordered_list_4(self):
        """Test unordered list conversion"""
        markdown = """* Item 1
* Item 2
* Item 3"""
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "ul")
        expected_html = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        self.assertEqual(node.children[0].to_html(), expected_html)

    def test_markdown_to_html_node_code_block_5(self):
        """Test code block conversion"""
        markdown = "```\nprint('hello')\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(
            node.children[0].to_html(),
            "<pre><code>print('hello')</code></pre>"
        )

    def test_markdown_to_html_node_mixed_content_6(self):
        """Test mixed content conversion"""
        markdown = """# Header

This is a paragraph.

* List item 1
* List item 2"""
        
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        expected = "<div><h1>Header</h1><p>This is a paragraph.</p><ul><li>List item 1</li><li>List item 2</li></ul></div>"
        self.assertEqual(html, expected)
