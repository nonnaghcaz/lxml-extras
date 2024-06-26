"""Extractors for lxml.etree._Element and lxml.etree._ElementTree objects."""

from typing import Any, Optional, Union

from lxml.etree import _Element, _ElementTree

from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import (
    InvalidXpathAttributeError,
    InvalidXpathError,
    NoXpathAttributesfoundError,
    XpathTooShortError,
)
from lxml_extras.utils.misc import is_numeric


def extract_attributes(
    tree: Union[_Element, _ElementTree],
    xpath: str,
    *,
    default: Optional[Any] = None,  # noqa: ANN401
    errors: Union[OnError, str] = OnError.RAISE,
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Extract attributes from an lxml element or tree using an xpath."""
    if (
        not xpath
        or not (xpath_parts := xpath.strip().split("/"))
        or not (xpath_parts := ["/".join(xpath_parts[:-1]), xpath_parts[-1]])
        or len(xpath_parts) <= 1
        or not xpath_parts[-1]
    ):
        if errors == OnError.RAISE:
            raise XpathTooShortError
        return default

    xpath_base = "/".join(xpath_parts[:-1])
    xpath_attr = xpath_parts[-1]

    # check if the attribute is text() or @attribute
    if xpath_attr == "text()" or xpath_attr.startswith("@"):
        try:
            attributes = tree.xpath(f"{xpath_base}/{xpath_attr}")
        except Exception as ex:
            if errors == OnError.RAISE:
                raise InvalidXpathError from ex
            return default
    else:
        if errors == OnError.RAISE:
            raise InvalidXpathAttributeError
        return default

    if not attributes:
        if errors == OnError.RAISE:
            raise NoXpathAttributesfoundError
        return default

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
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Extract links from an lxml element or tree using an xpath."""
    return extract_attributes(
        tree,
        xpath=xpath,
        default=default,
        errors=errors,
        limit=limit,
    )


def extract_images(
    tree: Union[_Element, _ElementTree],
    xpath: str = "//img/@src",
    *,
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Extract images from an lxml element or tree using an xpath."""
    return extract_attributes(
        tree,
        xpath=xpath,
        default=default,
        errors=errors,
        limit=limit,
    )


def extract_first_image(
    tree: Union[_Element, _ElementTree],
    xpath: str = "//img/@src",
    *,
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
) -> Optional[str]:
    """Extract the first image from an lxml element or tree using an xpath."""
    images = extract_images(tree, xpath, default=default, errors=errors, limit=1)
    if isinstance(images, list):
        return images[0]
    return images
