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
    errors: OnError = "raise",
) -> Optional[str]:
    """Convert an lxml node or tree to a string."""
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
    """Remove blank text from an lxml node or tree."""
    for element in node.iter():
        if element.text and element.text.strip() == "":
            element.text = None
    return node
