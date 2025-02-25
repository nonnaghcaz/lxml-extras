"""Tests for the lxml_extras.extractors module."""

import pytest
from lxml import html

from lxml_extras.extractors import (
    extract_attributes,
    extract_first_image,
    extract_images,
    extract_links,
    extract_tables,
)
from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import (
    InvalidXpathAttributeError,
    InvalidXpathError,
    NoXpathAttributesFoundError,
    XpathTooShortError,
)


def test_extract_links() -> None:
    """Test extract_links."""
    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="https://example.org">Example</a>
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    assert extract_links(tree) == [
        "https://example.com",
        "https://example.org",
        "https://example.net",
    ]
    assert extract_links(tree, limit=2) == [
        "https://example.com",
        "https://example.org",
    ]


def test_extract_images() -> None:
    """Test extract_images."""
    tree = html.fromstring(
        """
        <html>
            <body>
                <img src="https://example.com/image1.jpg" />
                <img src="https://example.org/image2.jpg" />
                <img src="https://example.net/image3.jpg" />
            </body>
        </html>
        """,
    )
    assert extract_images(tree) == [
        "https://example.com/image1.jpg",
        "https://example.org/image2.jpg",
        "https://example.net/image3.jpg",
    ]
    assert extract_images(tree, limit=2) == [
        "https://example.com/image1.jpg",
        "https://example.org/image2.jpg",
    ]


def test_extract_first_image() -> None:
    """Test extract_first_image."""
    tree = html.fromstring(
        """
        <html>
            <body>
                <img src="https://example.com/image1.jpg" />
                <img src="https://example.org/image2.jpg" />
                <img src="https://example.net/image3.jpg" />
            </body>
        </html>
        """,
    )
    assert extract_first_image(tree) == "https://example.com/image1.jpg"

    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="https://example.org">Example</a>
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    with pytest.raises(NoXpathAttributesFoundError):
        extract_first_image(tree)

    tree = html.fromstring(
        """
        <html>
            <body>
                <img src="https://example.com/image1.jpg" />
                <a href="https://example.org">Example</a>
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    assert extract_first_image(tree) == "https://example.com/image1.jpg"

    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <img src="https://example.org/image2.jpg" />
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    assert extract_first_image(tree) == "https://example.org/image2.jpg"

    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="https://example.org">Example</a>
                <img src="https://example.net/image3.jpg" />
            </body>
        </html>
        """,
    )
    assert extract_first_image(tree) == "https://example.net/image3.jpg"

    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="https://example.org">Example</a>
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    assert extract_first_image(tree, errors=OnError.IGNORE) is None


def test_extract_attributes() -> None:
    """Test extract_attributes."""
    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="https://example.org">Example</a>
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    assert extract_attributes(tree, "//a/@href") == [
        "https://example.com",
        "https://example.org",
        "https://example.net",
    ]
    assert extract_attributes(tree, "//a/@href", limit=2) == [
        "https://example.com",
        "https://example.org",
    ]

    tree = html.fromstring(
        """
        <html>
            <body>
                <img src="https://example.com/image1.jpg" />
                <img src="https://example.org/image2.jpg" />
                <img src="https://example.net/image3.jpg" />
            </body>
        </html>
        """,
    )
    assert extract_attributes(tree, "//img/@src") == [
        "https://example.com/image1.jpg",
        "https://example.org/image2.jpg",
        "https://example.net/image3.jpg",
    ]
    assert extract_attributes(tree, "//img/@src", limit=2) == [
        "https://example.com/image1.jpg",
        "https://example.org/image2.jpg",
    ]

    tree = html.fromstring(
        """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="https://example.org">Example</a>
                <a href="https://example.net">Example</a>
            </body>
        </html>
        """,
    )
    assert extract_attributes(tree, "//a/@href", limit=2) == [
        "https://example.com",
        "https://example.org",
    ]

    tree = html.fromstring(
        """
        <html>
            <body>
                <img src="https://example.com/image1.jpg" />
                <img src="https://example.org/image2.jpg" />
                <img src="https://example.net/image3.jpg" />
            </body>
        </html>
        """,
    )
    assert extract_attributes(tree, "//img/@src", limit=2) == [
        "https://example.com/image1.jpg",
        "https://example.org/image2.jpg",
    ]

    with pytest.raises(NoXpathAttributesFoundError):
        extract_attributes(tree, "//a/@href", errors=OnError.RAISE)

    assert extract_attributes(tree, "//a/@href", errors=OnError.IGNORE) is None

    with pytest.raises(XpathTooShortError):
        extract_attributes(tree, "", errors=OnError.RAISE)

    assert extract_attributes(tree, "", errors=OnError.IGNORE) is None

    assert extract_attributes(tree, "a", errors=OnError.IGNORE) is None

    with pytest.raises(InvalidXpathAttributeError):
        extract_attributes(tree, "//a", errors="raise")

    assert extract_attributes(tree, "//img", errors="ignore") is None

    with pytest.raises(InvalidXpathError):
        extract_attributes(tree, "//+q/@i", errors=OnError.RAISE)

    assert extract_attributes(tree, "//+q/@i", errors=OnError.IGNORE) is None
