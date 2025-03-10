import unittest

#from texnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

def self_test():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)
    node2 = TextNode("This is _absolutely_ insane LOL", TextType.TEXT )
    new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
    print(new_nodes2)
    node3 = TextNode("**This** is not a fun one", TextType.TEXT)
    new_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
    self.assertNotEqual(node3, node2)

if __name__ == "__main__":
    unittest.main()
