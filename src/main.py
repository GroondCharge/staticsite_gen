print("hello world")
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
def main():
    #print(TextType.BOLD.value)
    #newNode = TextNode("hello", TextType.BOLD )
    #print(newNode)
    theprops = {
                "href" : "https://google.com",
                "target" : "deadly_targe_lol",
                "color" : "a_perfect_color",
                  }
    numerouno = HTMLNode("p", "halozivjohalo", None, theprops)
    #print(numerouno.props_to_html())
    #print(numerouno.__repr__())
    node = TextNode("This is a text node", TextType.IMAGE, "https://url.to.insane.img")
    html_node = text_node_to_html_node(node)
    print(node)
    print(html_node.__repr__())
def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode("img", "", {
                "src" : text_node.url,
                "alt" : text_node.text
                })
        case TextType.LINK:
            return LeafNode("a", text_node.text, {
                "href" : text_node.url,
                })
        case _:
            raise Exception("None of the possible types")
main()
