"""Extra stringification for lxml."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional, Union

from lxml import html

from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import StringifyError

if TYPE_CHECKING:
    from lxml.etree import _Element, _ElementTree  # pragma: no cover


def to_string(
    node: Union[_Element, _ElementTree],
    *,
    exclude_own_tag: bool = True,
    default: Optional[str] = None,
    errors: Union[OnError, str] = "raise",
) -> Optional[str]:
    """Convert an lxml node or tree to a string, optionally excluding its own tag.

    :param node: The lxml node or tree to convert.
    :type node: Union[_Element, _ElementTree]
    :param exclude_own_tag: If True, excludes the node's own tag from the output. Defaults to True.
    :type exclude_own_tag: bool
    :param default: The default value to return in case of an error or if the node is empty. Defaults to None.
    :type default: Optional[str]
    :param errors: The error handling strategy. Defaults to "raise".
    :type errors: Union[OnError, str]
    :return: The stringified node or the default value in case of an error or if the node is empty.
    :rtype: Optional[str]
    :raises StringifyError: If errors is set to OnError.RAISE and an error occurs during stringification.

    >>> from lxml import etree
    >>> html = '<root><a href="link1">Link 1</a><a href="link2">Link 2</a></root>'
    >>> tree = etree.ElementTree(etree.fromstring(html))
    >>> to_string(tree)
    '<a href="link1">Link 1</a><a href="link2">Link 2</a>'
    """  # noqa: E501
    errors = OnError.from_any(errors)
    if node is None or (len(node) == 0 and not getattr(node, "text", None)):
        if errors == OnError.RAISE:
            raise StringifyError
        return default
    node.attrib.clear()

    node = remove_blank_node_text(node)
    stringified = html.tostring(node).decode("utf-8")
    for pattern, replace in {r"\n|\r": "", r">\s*": ">"}.items():
        stringified = re.sub(pattern, replace, stringified)
    if exclude_own_tag:
        opening_tag = len(node.tag) + 2
        closing_tag = -(len(node.tag) + 3)
        stringified = stringified[opening_tag:closing_tag]
    return stringified


def remove_blank_node_text(
    node: Union[_Element, _ElementTree],
) -> Union[_Element, _ElementTree]:
    """Remove blank text from an lxml node or tree to clean up the output.

    :param node: The lxml node or tree from which to remove blank text.
    :type node: Union[_Element, _ElementTree]
    :return: The node or tree with blank text removed.
    :rtype: Union[_Element, _ElementTree]

    >>> from lxml import etree
    >>> html = '<root><a href="link1">Link 1</a><a href="link2">Link 2</a></root>'
    >>> tree = etree.ElementTree(etree.fromstring(html))
    >>> remove_blank_node_text(tree)
    <Element root at 0x7f7f7f7f7f7f>
    """
    for element in node.iter():
        if element.text and element.text.strip() == "":
            element.text = None
    return node
