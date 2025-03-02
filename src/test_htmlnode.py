import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHtmlNode(unittest.TestCase):
    def test_generator(self):
        theprops = {
                "href" : "https://google.com",
                "target" : "deadly_targe_lol",
                "color" : "a_perfect_color",
                }
        theprops2 = {
                "target" : "targeted",
                "color_1" : "green",
                "href" : "http://insane.url",
                }
        numerouno = HTMLNode("p", "halozivjohalo", None, theprops)
        numerodue = HTMLNode("h", "insane_lol", None, theprops2)
        self.assertNotEqual(numerouno, numerodue)
        self.assertFalse(numerouno.children)
    def test_leaf_to_html_p(self):
        heprops2 = {
                  "target" : "targeted",
                  "color_1" : "green",
                  "href" : "http://insane.url",
                  }
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode("p", "Do not click", heprops2)
        self.assertNotEqual(node3, node2)
        #print(node3.to_html())
        #print(node2.to_html())
        node123 = ParentNode(
        "p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],
        )
        #print(node123.__repr__())
        #print(node123.to_html())
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        #print(child_node)
        #print(parent_node)
        self.assertEqual(
                    parent_node.to_html(),
                    "<div><span><b>grandchild</b></span></div>",
                        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
if __name__ == "__main__":
    unittest.main()
