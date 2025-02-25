"""Tests for the lxml_extras.stringify module."""

import pytest
from lxml import etree

from lxml_extras.stringify import to_string
from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import StringifyError


def test_to_string() -> None:
    """Test to_string."""
    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.HTML(
        """
        <html>
            <body>
                <p>Example</p>
            </body>
        </html>
        """,
        parser=parser,
    )
    assert to_string(tree) == "<body><p>Example</p></body>"
    assert (
        to_string(tree, exclude_own_tag=False)
        == "<html><body><p>Example</p></body></html>"
    )
    assert to_string(tree[0]) == "<p>Example</p>"
    assert to_string(tree[0], exclude_own_tag=False) == "<body><p>Example</p></body>"
    assert to_string(tree[0][0]) == "Example"
    assert to_string(tree[0][0], exclude_own_tag=False) == "<p>Example</p>"
    assert to_string(tree[0][0], exclude_own_tag=True) == "Example"

    with pytest.raises(StringifyError):
        to_string(None, errors=OnError.RAISE)

    assert to_string(None, errors=OnError.IGNORE) is None
    assert to_string(None, errors=OnError.IGNORE, default="default") == "default"
