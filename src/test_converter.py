import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("linking google", TextType.LINK, "https://link.2.google.kao")
        node3 = TextNode("italic text", TextType.ITALIC)
        node4 = TextNode("Yeah boy", TextType.IMAGE, "https://linkin.2.park")
        node5 = TextNode("this i scode", TextType.CODE, "http://what.iflink")
        html_node5 = text_node_to_html_node(node5)
        html_node4 = text_node_to_html_node(node4)
        html_node3 = text_node_to_html_node(node3)
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        print(html_node5.__repr__())
        print(html_node2.__repr__())
        print(html_node3.__repr__())
        print(html_node4.__repr__())
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.value, "linking google")

if __name__ == "__main__":
    unittest.main()
