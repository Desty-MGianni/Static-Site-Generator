from enum import Enum, auto
from re import match

from src.helpers_inline import text_node_to_html_node, text_to_textnodes
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType


class BlockType(Enum):
    PAR = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UL = auto()
    OL = auto()


def block_to_blockType(block: str) -> BlockType:

    if match(r"#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines: list[str] = block.split("\n")

    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.UL

    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.OL

    return BlockType.PAR


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks: list[str] = markdown.split("\n\n")
    return [block.strip() for block in raw_blocks if block != ""]


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    children: list[HTMLNode] = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children


def _help_block_head(block: str) -> HTMLNode:
    level: int = block.count("#", 0, 6)
    content: str = block.strip("# ").strip()
    return ParentNode(f"h{level}", text_to_children(content))


def _help_block_lists(block: str, block_type: BlockType) -> HTMLNode:
    lines: list[str] = block.split("\n")
    items: list[HTMLNode] = []
    for line in lines:
        parts: list[str] = line.split(" ", 1)
        if len(parts) > 1:
            content: str = parts[1]
            items.append(ParentNode("li", text_to_children(content)))
    tag: str = "ol" if block_type == BlockType.OL else "ul"
    return ParentNode(tag, items)


def _help_block_code(block: str) -> HTMLNode:
    content: str = block[3:-3].strip("\n") + "\n"
    code_leaf: LeafNode = text_node_to_html_node(TextNode(content, TextType.TEXT))
    code_node = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code_node])


def _help_bloc_quote(block: str) -> HTMLNode:
    lines: list[str] = block.split("\n")
    clean_lines: list[str] = [line.lstrip(">").strip() for line in lines]
    content = " ".join(clean_lines)
    return ParentNode("blockquote", text_to_children(content))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    block_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type: BlockType = block_to_blockType(block)

        match block_type:
            case BlockType.HEADING:
                block_nodes.append(_help_block_head(block))
            case BlockType.UL:
                block_nodes.append(_help_block_lists(block, BlockType.UL))
            case BlockType.OL:
                block_nodes.append(_help_block_lists(block, BlockType.OL))
            case BlockType.CODE:
                block_nodes.append(_help_block_code(block))
            case BlockType.QUOTE:
                block_nodes.append(_help_bloc_quote(block))
            case BlockType.PAR:
                content: str = block.replace("\n", " ")
                block_nodes.append(ParentNode("p", text_to_children(content)))

    parent: ParentNode = ParentNode("div", block_nodes)
    return parent
