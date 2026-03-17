from re import findall
from typing import Callable

from src.htmlnode import LeafNode
from src.textnode import TextNode, TextType

# TODO: Create the parent function that will handle the recursion (for nested delimiters)


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise Exception(
            "the value of property text_node.text_type is not in the TextType Enum"
        )

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise Exception(f"This node of type {text_node.text_type} has no url")
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMG:
            if text_node.url is None:
                raise Exception(f"This node of type {text_node.text_type} has no url")
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    if not old_nodes:
        return []

    new_nodes: list[TextNode] = []

    for node in old_nodes:

        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if not delimiter or delimiter not in node.text:
            new_nodes.append(node)
            continue

        text_split: list[str] = node.text.split(delimiter)

        if len(text_split) % 2 == 0:
            raise Exception(
                f"Invalid Markdown syntax. \nMatching closing delimiter {delimiter} not found. text: {node.text}"
            )

        for i, text in enumerate(text_split):
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # explanation regex:
    # 1. find a !
    # 2. has a group with [] directly after
    # 3. has a group with () directly after
    matches: list[tuple[str, str]] = findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # explanation regex:
    # 1. Dont find !
    # 2. has a group with []
    # 3. has a group with () directly
    matches: list[tuple[str, str]] = findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text
    )
    return matches


def _split_nodes_regexp(
    old_nodes: list[TextNode], extract_func: Callable, text_type: TextType
):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text: str = node.text

        matches: list[tuple[str, str]] = extract_func(current_text)
        if not matches:
            new_nodes.append(node)
            continue

        for alt_text, url in matches:

            delimiter: str = ""
            if text_type is TextType.IMG:
                delimiter = f"![{alt_text}]({url})"
            elif text_type is TextType.LINK:
                delimiter = f"[{alt_text}]({url})"
            else:
                raise Exception(f"Error occured when assigning delimiters for {node}")

            sections: list[str] = current_text.split(delimiter, maxsplit=1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, text_type, url))
            current_text = sections[1]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_regexp(old_nodes, extract_markdown_images, TextType.IMG)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_regexp(old_nodes, extract_markdown_links, TextType.LINK)


def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    text_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
