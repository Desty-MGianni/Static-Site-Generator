import unittest

from src.helpers_inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from src.textnode import TextNode, TextType

# TODO: IL FAUT FAIRE PLUS DE TEST POUR VERIFIE LE MAXIMUM DE CAS DIFFERENTS


class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})
        self.assertEqual(
            html_node.to_html(), '<a href="www.google.com">This is a text node</a>'
        )

    def test_img(self):
        node = TextNode("Text image", TextType.IMG, "https://placehold.co/200")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://placehold.co/200", "alt": "Text image"}
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://placehold.co/200" alt="Text image"></img>',
        )


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_text(self):
        node1 = TextNode("Salut les gars", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "", TextType.TEXT)
        self.assertEqual(len(nodes), 1)
        for node in nodes:
            self.assertEqual(node.text, "Salut les gars")
            self.assertEqual(node.text_type, TextType.TEXT)

    def test_bold(self):
        node1 = TextNode("Salut **les** gars", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)

        expected_texts: list[str] = ["Salut ", "les", " gars"]
        expected_types: list[TextType] = [TextType.TEXT, TextType.BOLD, TextType.TEXT]
        self.assertEqual(len(nodes), 3)
        for i, node in enumerate(nodes):
            self.assertEqual(node.text, expected_texts[i])
            self.assertEqual(node.text_type, expected_types[i])

    def test_multiple_bold(self):
        node1 = TextNode("Salut **les** super **mega** bros", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)

        expected_texts: list[str] = ["Salut ", "les", " super ", "mega", " bros"]
        expected_types: list[TextType] = [
            TextType.TEXT,
            TextType.BOLD,
            TextType.TEXT,
            TextType.BOLD,
            TextType.TEXT,
        ]

        self.assertEqual(len(nodes), 5)
        for i, node in enumerate(nodes):
            self.assertEqual(node.text, expected_texts[i])
            self.assertEqual(node.text_type, expected_types[i])

    def test_start_bold(self):
        node1 = TextNode("**Salut** les gars", TextType.TEXT)
        nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)

        expected_texts: list[str] = ["Salut", " les gars"]
        expected_types: list[TextType] = [TextType.BOLD, TextType.TEXT]

        self.assertEqual(len(nodes), 2)
        for i, node in enumerate(nodes):
            self.assertEqual(node.text, expected_texts[i])
            self.assertEqual(node.text_type, expected_types[i])

    def test_multiple_nodes(self):
        node1 = TextNode("Salut les **gars**", TextType.TEXT)
        node2 = TextNode("Comment **ca** va?", TextType.TEXT)
        nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)

        expected_texts: list[str] = ["Salut les ", "gars", "Comment ", "ca", " va?"]
        expected_types: list[TextType] = [
            TextType.TEXT,
            TextType.BOLD,
            TextType.TEXT,
            TextType.BOLD,
            TextType.TEXT,
        ]

        self.assertEqual(len(nodes), 5)
        for i, node in enumerate(nodes):
            self.assertEqual(node.text, expected_texts[i])
            self.assertEqual(node.text_type, expected_types[i])


class TestExtractImgAndLink(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a first [link](https://google.com) and a second [link](https://youtube.com)"
        )
        self.assertListEqual(
            [("link", "https://google.com"), ("link", "https://youtube.com")], matches
        )


class TestSplitNodeImageAndLink(unittest.TestCase):
    def test_img(self):
        node1 = TextNode("Here is an ![image](ouais.png)", TextType.TEXT)
        nodes = split_nodes_image([node1])
        self.assertEqual(len(nodes), 2)
        self.assertListEqual(
            nodes,
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "ouais.png"),
            ],
        )

    def test_multiple_img(self):
        node1 = TextNode(
            "Here is an ![image](ouais.png) and another ![image2](non.png)",
            TextType.TEXT,
        )
        nodes = split_nodes_image([node1])
        self.assertEqual(len(nodes), 4)
        self.assertListEqual(
            nodes,
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "ouais.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image2", TextType.IMG, "non.png"),
            ],
        )

    def test_multiple_links(self):
        node1 = TextNode(
            "Here is a [link](www.google.com) and another [link2](www.youtube.com)",
            TextType.TEXT,
        )
        nodes = split_nodes_link([node1])
        self.assertEqual(len(nodes), 4)
        self.assertListEqual(
            nodes,
            [
                TextNode("Here is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "www.youtube.com"),
            ],
        )

    def test_mixed_text(self):
        node1 = TextNode(
            "Here is an ![image](ouais.png) and a [link](www.google.com)", TextType.TEXT
        )
        nodes = split_nodes_image([node1])
        self.assertEqual(len(nodes), 3)
        self.assertListEqual(
            nodes,
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "ouais.png"),
                TextNode(" and a [link](www.google.com)", TextType.TEXT),
            ],
        )

    def test_mixed_text2(self):
        node1 = TextNode(
            "Here is an ![image](ouais.png) and a [link](www.google.com)", TextType.TEXT
        )
        nodes = split_nodes_link([node1])
        self.assertEqual(len(nodes), 2)
        self.assertListEqual(
            nodes,
            [
                TextNode("Here is an ![image](ouais.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
            ],
        )


class TestTextToTextNode(unittest.TestCase):
    def test_mix_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_glued(self):
        text = "**Bold**_Italic_![img](url.png)"
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("Bold", TextType.BOLD),
                TextNode("Italic", TextType.ITALIC),
                TextNode("img", TextType.IMG, "url.png"),
            ],
        )

    def test_start_and_end(self):
        text = "![image](url.png) is at the start and **bold** is at the end"
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("image", TextType.IMG, "url.png"),
                TextNode(" is at the start and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" is at the end", TextType.TEXT),
            ],
        )

    def test_plain_text(self):
        text = "Just a normal text"
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(nodes, [TextNode("Just a normal text", TextType.TEXT)])

    def test_ditto(self):
        text = "Here is an ![img](url.png) and the same ![img](url.png)"
        nodes: list[TextNode] = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("img", TextType.IMG, "url.png"),
                TextNode(" and the same ", TextType.TEXT),
                TextNode("img", TextType.IMG, "url.png"),
            ],
        )
