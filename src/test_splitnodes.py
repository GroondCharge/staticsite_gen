import unittest
from textnode import TextNode, TextType
#from texnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
class TestSplitNodes(unittest.TestCase):
    def test_thestuff(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        #print(new_nodes)
        node2 = TextNode("This is _absolutely_ insane LOL", TextType.TEXT )
        new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        #print(new_nodes2)
        node3 = TextNode("**This** is not a fun one", TextType.TEXT)
        new_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
        self.assertNotEqual(node3, node2)
        #print(new_nodes3)
class TestSplitNodesLink(unittest.TestCase):
    def test_basic_splitting(self):
        nodes = [
            TextNode("[text1](https://deez)[nuts](https://lol)", TextType.TEXT),
            TextNode("text [a](x)", TextType.TEXT),
            TextNode("a](x) text", TextType.TEXT)
        ]
        
        expected_output = [
            TextNode("text1", TextType.LINK, "https://deez"),
            TextNode("nuts", TextType.LINK, "https://lol"),
            TextNode("text ", TextType.TEXT, None),
            TextNode("a", TextType.LINK, "x"),
            TextNode("a](x) text", TextType.TEXT, None)
        ]
        
        self.assertEqual(split_nodes_link(nodes), expected_output)

    def test_no_links(self):
        nodes = [
            TextNode("plain text", TextType.TEXT),
            TextNode("another plain text", TextType.TEXT)
        ]
        expected_output = nodes  # Should remain unchanged
        self.assertEqual(split_nodes_link(nodes), expected_output)

    def test_only_links(self):
        nodes = [
            TextNode("[link1](http://example.com)", TextType.TEXT),
            TextNode("[link2](https://site.com)", TextType.TEXT)
        ]
        expected_output = [
            TextNode("link1", TextType.LINK, "http://example.com"),
            TextNode("link2", TextType.LINK, "https://site.com")
        ]
        self.assertEqual(split_nodes_link(nodes), expected_output)
    
    def test_mixed_text_and_links(self):
        nodes = [
            TextNode("hello [world](http://example.com)!", TextType.TEXT)
        ]
        expected_output = [
            TextNode("hello ", TextType.TEXT, None),
            TextNode("world", TextType.LINK, "http://example.com"),
            TextNode("!", TextType.TEXT, None)
        ]
        #print(f"heres the deal {nodes}")
        self.assertEqual(split_nodes_link(nodes), expected_output)

    def test_broken_markdown(self):
        nodes = [
            TextNode("[notalink](missingend", TextType.TEXT),
            TextNode("[unclosed](https://test", TextType.TEXT)
        ]
        expected_output = nodes  # Should remain unchanged as they are invalid
        self.assertEqual(split_nodes_link(nodes), expected_output)

#testing split images markdown

class TestSplitNodesImage(unittest.TestCase):
    def test_basic_image_extraction(self):
        nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        
        expected_output = [
            TextNode("This is text with an ", TextType.TEXT, None),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        
        self.assertEqual(split_nodes_image(nodes), expected_output)
    
    def test_no_images(self):
        nodes = [
            TextNode("Just some plain text.", TextType.TEXT),
            TextNode("More text with no images.", TextType.TEXT)
        ]
        expected_output = nodes  # Should remain unchanged
        self.assertEqual(split_nodes_image(nodes), expected_output)

    def test_multiple_images(self):
        nodes = [
            TextNode("Check this ![img1](http://example.com/img1.png) and this ![img2](http://example.com/img2.png)", TextType.TEXT)
        ]
        
        expected_output = [
            TextNode("Check this ", TextType.TEXT, None),
            TextNode("img1", TextType.IMAGE, "http://example.com/img1.png"),
            TextNode(" and this ", TextType.TEXT, None),
            TextNode("img2", TextType.IMAGE, "http://example.com/img2.png")
        ]
        
        self.assertEqual(split_nodes_image(nodes), expected_output)
    
    def test_mixed_text_and_images(self):
        nodes = [
            TextNode("Before ![pic](http://img.com/pic.jpg) after", TextType.TEXT)
        ]
        
        expected_output = [
            TextNode("Before ", TextType.TEXT, None),
            TextNode("pic", TextType.IMAGE, "http://img.com/pic.jpg"),
            TextNode(" after", TextType.TEXT, None)
        ]
        
        self.assertEqual(split_nodes_image(nodes), expected_output)
    
    def test_broken_markdown(self):
        nodes = [
            TextNode("![broken](missingend", TextType.TEXT),
            TextNode("![unclosed](http://test", TextType.TEXT)
        ]
        expected_output = nodes  # Should remain unchanged as they are invalid
        self.assertEqual(split_nodes_image(nodes), expected_output)

#testing split_nodes_image

class TestTextToTextNodes(unittest.TestCase):
    def test_basic_text(self):
        text = "This is a simple text."
        expected_output = [
            TextNode("This is a simple text.", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)

    def test_text_with_link(self):
        text = "Visit [Google](https://google.com) for searching."
        expected_output = [
            TextNode("Visit ", TextType.TEXT, None),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" for searching.", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)
    
    def test_text_with_image(self):
        text = "Here is a ![cute cat](https://i.imgur.com/cat.jpg)."
        expected_output = [
            TextNode("Here is a ", TextType.TEXT, None),
            TextNode("cute cat", TextType.IMAGE, "https://i.imgur.com/cat.jpg"),
            TextNode(".", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)
    
    def test_mixed_elements(self):
        text = "Some _italic_ text, a `code block`, a ![dog](https://i.imgur.com/dog.jpg), and a [repo](https://github.com)."
        expected_output = [
            TextNode("Some ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text, a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(", a ", TextType.TEXT, None),
            TextNode("dog", TextType.IMAGE, "https://i.imgur.com/dog.jpg"),
            TextNode(", and a ", TextType.TEXT, None),
            TextNode("repo", TextType.LINK, "https://github.com"),
            TextNode(".", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)
    
    def test_bold_text(self):
        text = "This is **bold** text."
        expected_output = [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text.", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)
    
    def test_italic_text(self):
        text = "This is _italic_ text."
        expected_output = [
            TextNode("This is ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text.", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)
    
    def test_code_text(self):
        text = "Here is `some code`."
        expected_output = [
            TextNode("Here is ", TextType.TEXT, None),
            TextNode("some code", TextType.CODE, None),
            TextNode(".", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)
    
    def test_broken_markdown(self):
        text = "This is [not a link(https://example.com) and ![broken image](https://img.com"
        expected_output = [
            TextNode("This is [not a link(https://example.com) and ![broken image](https://img.com", TextType.TEXT, None)
        ]
        self.assertEqual(text_to_textnodes(text), expected_output)


if __name__ == "__main__":
    unittest.main()
