import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_bold_eq(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        node2 = TextNode("This is a BOLD text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_normal_eq(self):
        node = TextNode("This is a normal text node", TextType.NORMAL)
        node2 = TextNode("This is a normal text node", TextType.NORMAL)
        self.assertEqual(node, node2)


    def test_bold_normal_ne(self):
        node = TextNode("This is a BOLD text node", TextType.BOLD)
        node2 = TextNode("This is a normal text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)   

    def test_empty_string_eq(self):
        node = TextNode("", TextType.NORMAL)
        node2 = TextNode("", TextType.NORMAL)
        self.assertEqual(node, node2) 

    def test_default_instance_eq(self):
        node = TextNode()
        node2 = TextNode("", TextType.NORMAL, None)
        self.assertEqual(node, node2) 

    def test_empty_normal_ne(self):
        node = TextNode("", TextType.NORMAL)
        node2 = TextNode("This is a normal text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)


    def test_empty_URL_ne(self):
        node = TextNode("This is a normal text node", TextType.NORMAL, None)
        node2 = TextNode("This is a normal text node", TextType.NORMAL, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_URL_eq(self):
        node = TextNode("This is a normal text node", TextType.NORMAL, "https://www.boot.dev")
        node2 = TextNode("This is a normal text node", TextType.NORMAL, "https://www.boot.dev")
        self.assertEqual(node, node2)

   
if __name__ == "__main__":
    unittest.main()