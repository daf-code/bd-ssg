import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_value_eq(self):
        node = LeafNode("div", "Test", {})
        node2 = LeafNode("div", "Test", {})
        self.assertEqual(node, node2)

    def test_leafnode_value_neq(self):
        node = LeafNode("div", "Test", {})
        node2 = LeafNode("div", "Test2", {})
        self.assertNotEqual(node, node2)

    def test_leafnode_ptext_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node, node2)

    def test_leafnode_ptext_neq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of t3xts.")
        self.assertNotEqual(node, node2)

    def test_leafnode_to_html_basic(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leafnode_to_html_with_props(self):
        node = LeafNode("p", "This is a paragraph of text.", {"class": "paragraph"})
        self.assertEqual(node.to_html(), "<p class='paragraph'>This is a paragraph of text.</p>")
"""
    def test_leafnode_to_html_with_no_tag_no_props(self):
        node = LeafNode(None, "This is a segment of text.", None)
        self.assertEqual(node.to_html(), "This is a segment of text.")

    def test_leafnode_to_html_with_no_tag_with_props(self):
        node = LeafNode(None, "This is a paragraph classed but untagged as text.", {"class": "paragraph"})
        self.assertEqual(node.to_html(), "ValueError: Cannot have props without a tag")

    def test_leafnode_to_html_tag_no_value(self):
        node = LeafNode("p")
        self.assertEqual(node.to_html(), "ValueError: Leaf node value is required")

    def test_leafnode_to_html_with_no_value_with_tag_and_props(self):
        node = LeafNode("p", None, {"class": "paragraph"})
        self.assertEqual(node.to_html(), "ValueError: Leaf node value is required")
        
        

if __name__ == "__main__":
    unittest.main() """