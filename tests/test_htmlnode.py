import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "Hello, world!", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Hello, world!</a>')

    def test_node_to_html(self):
        node = HTMLNode("a", "salut", props={"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_tml_complete(self):
        node1 = LeafNode(
            tag="a",
            value="google.com",
            props={"class": "test_class", "id": "test_id", "href": "www.google.com"},
        )
        node2 = ParentNode(
            tag="div",
            props={"class": "test_class2", "id": "test_id2"},
            children=[node1],
        )
        node3 = ParentNode(
            tag="body", props={"class": "main_class", "id": "main_id"}, children=[node2]
        )
        self.assertEqual(
            node3.to_html(),
            '<body class="main_class" id="main_id"><div class="test_class2" id="test_id2"><a class="test_class" id="test_id" href="www.google.com">google.com</a></div></body>',
        )


if __name__ == "__main__":
    unittest.main()
