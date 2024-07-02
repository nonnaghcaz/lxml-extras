"""Extractors for lxml.etree._Element and lxml.etree._ElementTree objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import (
    InvalidXpathAttributeError,
    InvalidXpathError,
    NoXpathAttributesFoundError,
    XpathTooShortError,
)
from lxml_extras.utils.misc import is_numeric

if TYPE_CHECKING:
    from lxml.etree import _Element, _ElementTree


def extract_attributes(
    tree: Union[_Element, _ElementTree],
    xpath: str,
    *,
    errors: Union[OnError, str] = "raise",
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Extract attributes from an lxml element or tree using an xpath.

    :param tree: The lxml element or tree to extract attributes from.
    :type tree: Union[_Element, _ElementTree]
    :param xpath: The xpath expression to select the attributes.
    :type xpath: str
    :param errors: The error handling behavior. Defaults to "raise".
    :type errors: Union[OnError, str]
    :param limit: The maximum number of attributes to extract. Defaults to None.
    :type limit: Optional[int]
    :return: The list of extracted attributes, or None if no attributes found.
    :rtype: Optional[list[str]]
    :raises XpathTooShortError: If the xpath is too short.
    :raises InvalidXpathError: If the xpath is invalid.
    :raises InvalidXpathAttributeError: If the xpath attribute is invalid.
    :raises NoXpathAttributesFoundError: If no attributes are found.

    >>> from lxml import etree
    >>> html = '<root><a href="link1">Link 1</a><a href="link2">Link 2</a></root>'
    >>> tree = etree.ElementTree(etree.fromstring(html))
    >>> extract_attributes(tree, "//a/@href")
    ['link1', 'link2']
    """
    errors = OnError.from_any(errors)

    if (
        not xpath
        or not (xpath_parts := xpath.strip().split("/"))
        or not (xpath_parts := ["/".join(xpath_parts[:-1]), xpath_parts[-1]])
        or len(xpath_parts) <= 1
        or not xpath_parts[-1]
    ):
        if errors == OnError.RAISE:
            raise XpathTooShortError
        return None

    xpath_base = "/".join(xpath_parts[:-1])
    xpath_attr = xpath_parts[-1]

    # check if the attribute is text() or @attribute
    if xpath_attr == "text()" or xpath_attr.startswith("@"):
        try:
            attributes = tree.xpath(f"{xpath_base}/{xpath_attr}")
        except Exception as ex:
            if errors == OnError.RAISE:
                raise InvalidXpathError from ex
            return None
    else:
        if errors == OnError.RAISE:
            raise InvalidXpathAttributeError
        return None

    if not attributes:
        if errors == OnError.RAISE:
            raise NoXpathAttributesFoundError
        return None

    limit = (
        len(attributes)
        if (
            not limit
            or not is_numeric(limit)
            or (int_limit := int(float(limit))) <= 0
            or int_limit > len(attributes)
        )
        else int(float(limit))
    )

    return list(attributes)[:limit]


def extract_links(
    tree: Union[_Element, _ElementTree],
    xpath: str = "//a/@href",
    *,
    errors: Union[OnError, str] = "raise",
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Extract links from an lxml element or tree using an xpath.

    :param tree: The lxml element or tree to extract links from.
    :type tree: Union[_Element, _ElementTree]
    :param xpath: The xpath expression to select the links. Defaults to "//a/@href".
    :type xpath: str
    :param errors: The error handling behavior. Defaults to "raise".
    :type errors: Union[OnError, str]
    :param limit: The maximum number of links to extract. Defaults to None.
    :type limit: Optional[int]
    :return: The list of extracted links, or None if no links found.
    :rtype: Optional[list[str]]
    :raises XpathTooShortError: If the xpath is too short.
    :raises InvalidXpathError: If the xpath is invalid.
    :raises InvalidXpathAttributeError: If the xpath attribute is invalid.
    :raises NoXpathAttributesFoundError: If no attributes are found.

    >>> from lxml import etree
    >>> html = '<root><a href="link1">Link 1</a><a href="link2">Link 2</a></root>'
    >>> tree = etree.ElementTree(etree.fromstring(html))
    >>> extract_links(tree)
    ['link1', 'link2']
    """
    return extract_attributes(
        tree,
        xpath=xpath,
        errors=errors,
        limit=limit,
    )


def extract_images(
    tree: Union[_Element, _ElementTree],
    xpath: str = "//img/@src",
    *,
    errors: Union[OnError, str] = "raise",
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Extract images from an lxml element or tree using an xpath.

    :param tree: The lxml element or tree to extract images from.
    :type tree: Union[_Element, _ElementTree]
    :param xpath: The xpath expression to select the images. Defaults to "//img/@src".
    :type xpath: str
    :param errors: The error handling behavior. Defaults to "raise".
    :type errors: Union[OnError, str]
    :param limit: The maximum number of images to extract. Defaults to None.
    :type limit: Optional[int]
    :return: The list of extracted images, or None if no images found.
    :rtype: Optional[list[str]]
    :raises XpathTooShortError: If the xpath is too short.
    :raises InvalidXpathError: If the xpath is invalid.
    :raises InvalidXpathAttributeError: If the xpath attribute is invalid.
    :raises NoXpathAttributesFoundError: If no attributes are found.

    >>> from lxml import etree
    >>> html = '<root><img src="image1.jpg"/><img src="image2.jpg"/></root>'
    >>> tree = etree.ElementTree(etree.fromstring())
    >>> extract_images(tree)
    ['image1.jpg', 'image2.jpg']
    """
    return extract_attributes(
        tree,
        xpath=xpath,
        errors=errors,
        limit=limit,
    )


def extract_first_image(
    tree: Union[_Element, _ElementTree],
    xpath: str = "//img/@src",
    *,
    errors: Union[OnError, str] = "raise",
) -> Optional[str]:
    """Extract the first image from an lxml element or tree using an xpath.

    :param tree: The lxml element or tree to extract the first image from.
    :type tree: Union[_Element, _ElementTree]
    :param xpath: The xpath expression to select the images. Defaults to "//img/@src".
    :type xpath: str
    :param errors: The error handling behavior. Defaults to "raise".
    :type errors: Union[OnError, str]
    :return: The first extracted image, or None if no image found.
    :rtype: Optional[str]
    :raises XpathTooShortError: If the xpath is too short.
    :raises InvalidXpathError: If the xpath is invalid.
    :raises InvalidXpathAttributeError: If the xpath attribute is invalid.
    :raises NoXpathAttributesFoundError: If no attributes are found.

    >>> from lxml import etree
    >>> html = '<root><img src="image1.jpg"/><img src="image2.jpg"/></root>'
    >>> tree = etree.ElementTree(etree.fromstring(html))
    >>> extract_first_image(tree)
    'image1.jpg'
    """
    images = extract_images(tree, xpath, errors=errors, limit=1)
    if isinstance(images, list):
        return images[0]
    return images
