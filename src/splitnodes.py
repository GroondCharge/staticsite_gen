from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links, extract_bold
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown syntax. Section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_list.extend(split_nodes)
    return new_list
                
def split_nodes_link(old_nodes):
    extracted = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            extracted.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        for x,y in links:
            if not remaining_text:
                continue
            locator = f"[{x}]({y})"
            location = remaining_text.find(locator)
            if location != 0:
                extracted.append(TextNode(remaining_text[:location], TextType.TEXT))
            extracted.append(TextNode(x, TextType.LINK, y))
            remaining_text = remaining_text[location + len(locator):]
        if remaining_text:
            extracted.append(TextNode(remaining_text, TextType.TEXT))
    return extracted

def split_nodes_image(old_nodes):
    extracted = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            extracted.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        for x,y in images:
            if not remaining_text:
                continue
            locator = f"![{x}]({y})"
            location = remaining_text.find(locator)
            if location != 0:
                extracted.append(TextNode(remaining_text[:location], TextType.TEXT))
            extracted.append(TextNode(x, TextType.IMAGE, y))
            remaining_text = remaining_text[location + len(locator):]
        if remaining_text:
            extracted.append(TextNode(remaining_text, TextType.TEXT))
    return extracted


def text_to_textnodes(text):
    text_nodes = []
    text_nodes = split_nodes_image([TextNode(text, TextType.TEXT)])
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    return text_nodes

def markdown_to_blocks(markdown):
    return list(
                filter(lambda x: x, list(
                    map(lambda x: x.strip(),markdown.split("\n\n")))))

# md = """
# This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line





# - This is a list
# - with items
# """

# print(markdown_to_blocks(md))