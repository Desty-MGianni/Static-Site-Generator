import unittest

from src.helpers_block import (
    BlockType,
    block_to_blockType,
    markdown_to_blocks,
    markdown_to_html_node,
)
from src.htmlnode import HTMLNode


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md: str = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks: list[str] = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md: str = """
# Heading number 1

This is a paragraph under the heading number 1
This is the same paragraph on a new line

- First element in the list
- Second element in the list

# Heading number 2

![link to an image](image.png)
        """
        blocks: list[str] = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "# Heading number 1",
                "This is a paragraph under the heading number 1\nThis is the same paragraph on a new line",
                "- First element in the list\n- Second element in the list",
                "# Heading number 2",
                "![link to an image](image.png)",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block: str = "Here is a paragraph"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.PAR)

    def test_messy_ul(self):
        block: str = "- Here is a paragraph\nAnd another line in the paragraph"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.PAR)

    def test_ul(self):
        block: str = "- Here is the first element\n- Here is the second element"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.UL)

    def test_ol(self):
        block: str = "1. First element\n2. Second element"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.OL)

    def test_h1(self):
        block: str = "# Heading!"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_h3(self):
        block: str = "### Heading!"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_h6(self):
        block: str = "###### Heading!"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_quote(self):
        block: str = "> Here is a quote from someone:\n>Dont piss me off"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_fail_quote(self):
        block: str = ">Here is a quote:\nDont piss me off"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.PAR)

    def test_code(self):
        block: str = "```print(mommy.age)```"
        block_type: BlockType = block_to_blockType(block)
        self.assertEqual(block_type, BlockType.CODE)


class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md: str = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node: HTMLNode = markdown_to_html_node(md)
        html: str = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md: str = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node: HTMLNode = markdown_to_html_node(md)
        html: str = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_multiple_blocks(self):
        md: str = """
# Test level 1 heading

- Test list 1
- Test list 2
- Test list 3
        """
        node: HTMLNode = markdown_to_html_node(md)
        html: str = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Test level 1 heading</h1><ul><li>Test list 1</li><li>Test list 2</li><li>Test list 3</li></ul></div>",
        )
