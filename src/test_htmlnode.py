import unittest

from htmlnode import HTMLNode
# self, tag: str = None, value: str = None, children: list = None, props: dict = None



class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode_value_eq(self):
        node = HTMLNode("", "Test", [], {})
        node2 = HTMLNode("", "Test", [], {})
        self.assertEqual(node, node2)

    def test_HTMLNode_div_eq(self):
        node = HTMLNode("div", "Test", [], {})
        node2 = HTMLNode("div", "Test", [], {})
        self.assertEqual(node, node2)

    def test_HTMLNode_div_value1_neq(self):
        node = HTMLNode("div", "Test", [], {})
        node2 = HTMLNode("div", "Test2", [], {})
        self.assertNotEqual(node, node2)

    def test_HTMLNode_div_value_empty_neq(self):
        node = HTMLNode("div", "Test", [], {})
        node2 = HTMLNode("div", "", [], {})
        self.assertNotEqual(node, node2)

    def test_default_and_empty_instances_neq(self):
        node = HTMLNode()
        node2 = HTMLNode("", "", [], {})
        self.assertNotEqual(node, node2)

    def test_props_to_html_basic(self):
        node = HTMLNode("div", "Test", [], {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props1(self):
        node = HTMLNode("div", "Test", [], {"class": "test"})
        self.assertEqual(node.props_to_html(), " class='test'")

    def test_props_to_html_with_props2(self):
        node = HTMLNode("a", "Test", [], {"href": "https://www.google.com",
    "target": "_blank",})
        self.assertEqual(node.props_to_html(), " href='https://www.google.com' target='_blank'")

    def test_props_to_html_with_props3(self):
        node = HTMLNode("a", "Test", [], {"href": "https://www.google.com",
    "target": "_blank", "class": "test"})
        self.assertEqual(node.props_to_html(), " href='https://www.google.com' target='_blank' class='test'")

    def test_multiple_1(self):
        node = HTMLNode("a", "Test", [], {})
        node2 = HTMLNode("div", "Test", [], {})
        self.assertNotEqual(node, node2)

    def test_multiple_2(self):
        node = HTMLNode("div", "Test", [], {"class": "test"})
        node2 = HTMLNode("div", "Test", [], {"class": "test2"})
        self.assertNotEqual(node, node2)

    def test_children_1(self):
        node = HTMLNode("div", "Test", [])
        node_c_1 = HTMLNode("p", "Test Paragraph 1", [])
        node_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node.children = [node_c_1, node_c_2]
        node2 = HTMLNode("div", "Test", [])
        node2_c_1 = HTMLNode("p", "Test Paragraph 1", [])
        node2_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node2.children = [node2_c_1, node2_c_2]
        self.assertEqual(node, node2)

    def test_children_missing(self):
        node = HTMLNode("div", "Test", [])
        node_c_1 = HTMLNode("p", "Test Paragraph 1", [])
        node_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node.children = [node_c_1, node_c_2]
        node2 = HTMLNode("div", "Test", [])
        self.assertNotEqual(node, node2)

    def test_children_value_mismatch(self):
        node = HTMLNode("div", "Test", [])
        node_c_1 = HTMLNode("p", "Test Paragraph 1", [])
        node_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node.children = [node_c_1, node_c_2]
        node2 = HTMLNode("div", "Test", [])
        node2_c_1 = HTMLNode("p", "Test Paragraph 2", [])
        node2_c_2 = HTMLNode("p", "Test Paragraph 1", [])
        node2.children = [node2_c_1, node2_c_2]
        self.assertNotEqual(node, node2)

    def test_children_props_mismatch(self):
        node = HTMLNode("div", "Test", [])
        node_c_1 = HTMLNode("p", "Test Paragraph 1", [], {"class": "test"})
        node_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node.children = [node_c_1, node_c_2]
        node2 = HTMLNode("div", "Test", [])
        node2_c_1 = HTMLNode("p", "Test Paragraph 1", [])
        node2_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node2.children = [node2_c_1, node2_c_2]
        self.assertNotEqual(node, node2)

    def test_children_props_match(self):
        node = HTMLNode("div", "Test", [])
        node_c_1 = HTMLNode("p", "Test Paragraph 1", [], {"class": "test"})
        node_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node.children = [node_c_1, node_c_2]
        node2 = HTMLNode("div", "Test", [])
        node2_c_1 = HTMLNode("p", "Test Paragraph 1", [], {"class": "test"})
        node2_c_2 = HTMLNode("p", "Test Paragraph 2", [])
        node2.children = [node2_c_1, node2_c_2]
        self.assertEqual(node, node2)