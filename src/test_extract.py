import unittest

from extract import extract_markdown_images, extract_markdown_links

class TheUnitTest(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        #print("haloživjohalo")
    def test_basic_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "Check these images: ![First](https://example.com/first.jpg) and ![Second](https://example.com/second.jpg)"
        )
        self.assertListEqual([
            ("First", "https://example.com/first.jpg"),
            ("Second", "https://example.com/second.jpg")
        ], matches)

    def test_empty_alt_text(self):
        matches = extract_markdown_images(
            "Here is an image with no alt text: ![](https://example.com/image.jpg)"
        )
        self.assertListEqual([("", "https://example.com/image.jpg")], matches)

    def test_no_markdown_image(self):
        matches = extract_markdown_images(
            "This text has no images, just a URL: https://example.com"
        )
        self.assertListEqual([], matches)

    def test_malformed_markdown_no_closing_bracket(self):
        matches = extract_markdown_images(
            "This is an incorrect image format: ![broken(https://example.com/broken.jpg"
        )
        self.assertListEqual([], matches)

    def test_malformed_markdown_no_parentheses(self):
        matches = extract_markdown_images(
            "This is missing parentheses: ![alt text] https://example.com/image.jpg"
        )
        self.assertListEqual([], matches)

    def test_image_with_spaces_in_alt_text(self):
        matches = extract_markdown_images(
            "Here is an image with a long alt: ![This is an image](https://example.com/pic.jpg)"
        )
        self.assertListEqual([("This is an image", "https://example.com/pic.jpg")], matches)
#####
    def test_basic_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)
        #print("deeeeeeeez")
        #print(matches)

    def test_multiple_links(self):
        text = "[Google](https://google.com) [GitHub](https://github.com) [Python](https://python.org)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com"),
            ("Python", "https://python.org")
        ], matches)

    def test_empty_link_text(self):
        text = "Here is a link with no text: []() and another [valid](https://valid.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", ""), ("valid", "https://valid.com")], matches)

    def test_no_markdown_links(self):
        text = "This text has no links, just a URL: https://example.com"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_malformed_markdown_no_closing_bracket(self):
        text = "This is a broken link: [broken(https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_malformed_markdown_no_parentheses(self):
        text = "Missing parentheses: [alt text] https://example.com"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_link_with_spaces(self):
        text = "Check this out: [My website](https://example.com/my page)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("My website", "https://example.com/my page")], matches)

    def test_link_with_special_characters(self):
        text = "Some links: [C++ Docs](https://cplusplus.com), [Python & ML](https://python.com/ml?query=ai)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("C++ Docs", "https://cplusplus.com"),
            ("Python & ML", "https://python.com/ml?query=ai")
        ], matches)

    #print(text_extract_markdown_images)
if __name__ == "__main__":
    unittest.main()
