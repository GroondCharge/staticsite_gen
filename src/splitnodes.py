from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if old_node.text.count(str(delimiter)) % 2 != 0:
            raise Exception("Invalid markdown syntax")
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
        else:
            working = old_node.text.split(delimiter)
            if old_node.text[0] == delimiter[0]:
                #working = old_node.text.split(delimiter)
                counter = 0
                while counter < len(working):
                    #if counter == 0:
                    #    new_list.append(TextNode(working[counter], text_type))
                    if counter != 0:
                        if counter % 2 != 0:
                            new_list.append(TextNode(working[counter], text_type))
                        else:
                            new_list.append(TextNode(working[counter], TextType.TEXT))
                    counter += 1
            else:
                counter = 0
                while counter < len(working):
                    if counter == 0:
                        new_list.append(TextNode(working[counter], TextType.TEXT))
                    else:
                        if counter % 2 != 0:
                            new_list.append(TextNode(working[counter], text_type))
                        else:
                            new_list.append(TextNode(working[counter], TextType.TEXT))
                    counter += 1
        return new_list
                

#node = TextNode("This is text with a `code block` word", TextType.TEXT)
#new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#print(new_nodes)
#node2 = TextNode("This is _absolutely_ insane LOL", TextType.TEXT )
#new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
#print(new_nodes2)
#node3 = TextNode("**This** is not a fun one", TextType.TEXT)
#new_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
#print(new_nodes3)

#node5 = TextNode("ja **hehe hoho** hehe *haha* bla", TextType.TEXT)
#new_node5 = split_nodes_delimiter([node5], "**", TextType.BOLD)
#print(new_node5)

#node4 = TextNode("**this** is code with improper ** Syntax", TextType.BOLD)

#new_node4 = split_nodes_delimiter([node4], "**", TextType.BOLD)
#print(new_node4)

