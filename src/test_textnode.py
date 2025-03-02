import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("this is ay Noder node", TextType.CODE, "https://halo.si")
        node4 = TextNode("Text halo", TextType.TEXT)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node2)


if __name__ == "__main__":
    unittest.main()
