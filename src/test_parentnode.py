import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_parentnode_tag_eq(self):
        node = ParentNode("div", [], {})
        node2 = ParentNode("div", [], {})
        self.assertEqual(node, node2)

    def test_parentnode_tag_neq(self):
        node = ParentNode("div", [], {})
        node2 = ParentNode("p", [], {})
        self.assertNotEqual(node, node2)

     
    def test_parentnode_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_to_html_with_parent_node_in_div(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ], {}),
            ],
            )
        self.assertEqual(node.to_html(), "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>")

    def test_parentnode_to_html_with_parent_node_in_p(self):
        node = ParentNode(
            "p",
            [
                ParentNode("p", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ], {}),
                ParentNode("p", [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ], {}),
            ],
            )
        self.assertEqual(node.to_html(), "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")