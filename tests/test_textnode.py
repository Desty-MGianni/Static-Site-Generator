import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.IMG, url="234")
        node2 = TextNode("This is a text node", TextType.IMG, url="234")
        self.assertEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node", TextType.IMG, url="234")
        node2 = TextNode("this is a text node", TextType.IMG, url="234")
        self.assertNotEqual(node, node2)

    def test_neq3(self):
        node = TextNode("This is a text node", TextType.IMG, url="234")
        node2 = TextNode("This is a text node", TextType.IMG)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
