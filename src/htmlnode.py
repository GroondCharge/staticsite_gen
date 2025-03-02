from textnode import TextType
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    def props_to_html(self):
        if self.props == None:
            return ""
        string = ""
        for prop in self.props:
            string += f"{prop}=\"{self.props[prop]}\" "
        return string
    def __repr__(self):
        print(f"tag: {self.tag} \n value: {self.value}\nchildren: {self.children}\nprops_to_html: {self.props_to_html()} ")
    #def to_paragraph(string):
    #    return f"<p>{string}<\/p> "
    #def to_url(string):
    #    return f"href=\"{string}\" "
    #def to_heading(which_heading, heading):
    #    return f"<{which_heading}>{heading}<\/{which_heading}> "

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf node MUST have value")
        if not self.tag:
            print(self.value)
            return self.value
        #print(f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None,  children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("no tag provided")
        if not self.children:
            raise ValueError("No children provided to parent node")
        the_string = ""
        for child in self.children:
            #the_string += f"<{self.tag}{self.props_to_html()}>{child.to_html()}</{self.tag}>"
            the_string +=child.to_html()
        #print(the_string)
        return f"<{self.tag}{self.props_to_html()}>{the_string}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

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
