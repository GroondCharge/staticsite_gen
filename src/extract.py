import re
from textnode import TextNode

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_bold(text):
    return re.findall(r"\*\*([^\*]*)\*\*", text)
def extract_italic(text):
    return re.findall(r"", text)
