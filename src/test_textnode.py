import unittest

from textnode import TextNode, TextType

from extract import extract_markdown_images, extract_markdown_links

class TestExtract(unittest.TestCase):
    def text_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        print("haloživjohalo")
        self.assertEqual("halo", "Halo")
    #print(text_extract_markdown_images)

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
        #print("no ro")
        #self.assertEqual("halo", "Halo")


if __name__ == "__main__":
    unittest.main()
