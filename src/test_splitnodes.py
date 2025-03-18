import unittest
from textnode import TextNode, TextType
#from texnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes, markdown_to_blocks
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




class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_paragraph_split(self):
        """A simple example with two paragraphs separated by a blank line."""
        md = """
This is **bolded** paragraph

This is another paragraph
"""
        blocks = markdown_to_blocks(md)
        # We expect empty items removed.
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph",
            ],
        )

    def test_example_from_user(self):
        """The example the user provided with paragraphs, code, italics, and a list."""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_line_no_breaks(self):
        """Single line of text should produce a single block."""
        md = """Single line no breaks"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Single line no breaks"])

    def test_only_single_newlines(self):
        """No double line breaks, so everything is one block."""
        md = "Line one\nLine two\nLine three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line one\nLine two\nLine three"])

    def test_multiple_double_line_breaks(self):
        """Check that extra blank lines do not create empty blocks."""
        md = """
Para one

Para two


Para three
"""
        # We want to ensure we skip over empty lines.
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Para one",
                "Para two",
                "Para three",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        """Leading/trailing spaces should be stripped, and empty blocks removed."""
        md = """
   Leading spaces here   \n\nTrailing spaces here   \n"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Leading spaces here",
                "Trailing spaces here",
            ],
        )

    def test_list_items_no_blank_line(self):
        """No double breaks means all list items are in a single block."""
        md = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])

    def test_list_items_with_blank_line(self):
        """A blank line should split the list into two blocks."""
        md = """
- Item 1
- Item 2

- Item 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- Item 1\n- Item 2", "- Item 3"],
        )

    def test_long_paragraph_across_lines(self):
        """Single block split by double break."""
        md = """
This line is part one
and this line is part two

Now we start another paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This line is part one\nand this line is part two",
                "Now we start another paragraph.",
            ],
        )

    def test_empty_input(self):
        """Completely empty input should return an empty list."""
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


    
if __name__ == "__main__":
    unittest.main()
