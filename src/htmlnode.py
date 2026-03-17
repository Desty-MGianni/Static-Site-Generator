class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("Not Implemented")

    def props_to_html(self) -> str:
        s: str = ""
        if self.props:
            for prop, val in self.props.items():
                s += " "
                s += f'{prop}="{val}"'

        return s

    def __repr__(self) -> str:
        return f"""HTMLNode(
    tag={self.tag}
    value={self.value}
    children={self.children}
    props = {self.props}
 )
    """


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"""HTMLNode(
    tag={self.tag}
    value={self.value}
    props = {self.props}
 )
    """


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode doesn't have a tag")
        if self.children is None:
            raise ValueError(
                f"ParentNode should have children, but have {self.children} instead"
            )

        children_html: str = "".join(map(lambda child: child.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
