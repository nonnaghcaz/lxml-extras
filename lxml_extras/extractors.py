"""Extractors for lxml.etree._Element and lxml.etree._ElementTree objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import (
    InvalidXpathAttributeError,
    InvalidXpathError,
    NoElementsFoundError,
    NoXpathAttributesFoundError,
    XpathTooShortError,
)
from lxml_extras.utils.misc import is_numeric

if TYPE_CHECKING:
    from lxml.etree import _Element, _ElementTree


def extract_elements(
    tree: Union[_Element, _ElementTree],
    xpath: str,
    *,
    errors: Union[OnError, str] = "raise",
    limit: Optional[int] = None,
) -> Optional[list[_Element]]:
    """Extract elements from an lxml element or tree using an xpath.

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract elements from.
        xpath (str): The xpath expression to select the elements.
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".
        limit (Optional[int]): The maximum number of elements to extract. Defaults to None.

    Returns:
        Optional[list[_Element]]: The list of extracted elements, or None if no elements found.

    Raises:
        InvalidXpathError: If the xpath is invalid.
        NoElementsFoundError: If no elements are found.

    Examples:

        >>> from lxml import etree
        >>> html = '<root><a>Link 1</a><a>Link 2</a></root>'
        >>> tree = etree.ElementTree(etree.fromstring(html))
        >>> extract_elements(tree, "//a")
        [<Element a at 0x7f5f8b5d5b40>, <Element a at 0x7f5f8b5d5b90>]

    """
    errors = OnError.from_any(errors)
    try:
        elements = tree.xpath(xpath)
    except Exception as ex:
        if errors == OnError.RAISE:
            raise InvalidXpathError from ex
        return None

    if not elements:
        if errors == OnError.RAISE:
            raise NoElementsFoundError
        return None

    limit = (
        len(elements)
        if (
            not limit
            or not is_numeric(limit)
            or (int_limit := int(float(limit))) <= 0
            or int_limit > len(elements)
        )
        else int(float(limit))
    )

    return elements[:limit]


def extract_attributes(
    tree: Union[_Element, _ElementTree],
    xpath: str,
    *,
    errors: Union[OnError, str] = "raise",
    limit: Optional[int] = None,
) -> Optional[list[Any]]:
    """Extract attributes from an lxml element or tree using an xpath.

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract attributes from.
        xpath (str): The xpath expression to select the attributes.
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".
        limit (Optional[int]): The maximum number of attributes to extract. Defaults to None.

    Returns:
        Optional[list[str]]: The list of extracted attributes, or None if no attributes found.

    Raises:
        XpathTooShortError: If the xpath is too short.
        InvalidXpathError: If the xpath is invalid.
        InvalidXpathAttributeError: If the xpath attribute is invalid.
        NoXpathAttributesFoundError: If no attributes are found.

    Examples:

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

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract links from.
        xpath (str): The xpath expression to select the links. Defaults to "//a/@href".
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".
        limit (Optional[int]): The maximum number of links to extract. Defaults to None.

    Returns:
        Optional[list[str]]: The list of extracted links, or None if no links found.

    Raises:
        XpathTooShortError: If the xpath is too short.
        InvalidXpathError: If the xpath is invalid.
        InvalidXpathAttributeError: If the xpath attribute is invalid.
        NoXpathAttributesFoundError: If no attributes are found.

    Examples:

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

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract images from.
        xpath (str): The xpath expression to select the images. Defaults to "//img/@src".
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".
        limit (Optional[int]): The maximum number of images to extract. Defaults to None.

    Returns:
        Optional[list[str]]: The list of extracted images, or None if no images found.

    Raises:
        XpathTooShortError: If the xpath is too short.
        InvalidXpathError: If the xpath is invalid.
        InvalidXpathAttributeError: If the xpath attribute is invalid.
        NoXpathAttributesFoundError: If no attributes are found.

    Examples:

        >>> from lxml import etree
        >>> html = '<root><img src="image1.jpg"/><img src="image2.jpg"/></root>'
        >>> tree = etree.ElementTree(etree.fromstring(html))
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

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract the first image from.
        xpath (str): The xpath expression to select the images. Defaults to "//img/@src".
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".

    Returns:
        Optional[str]: The first extracted image, or None if no image found.

    Raises:
        XpathTooShortError: If the xpath is too short.
        InvalidXpathError: If the xpath is invalid.
        InvalidXpathAttributeError: If the xpath attribute is invalid.
        NoXpathAttributesFoundError: If no attributes are found.

    Examples:

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


def extract_tables(
    tree: Union[_Element, _ElementTree],
    base_xpath: str = "//table",
    *,
    has_headers: bool = True,
    errors: Union[OnError, str] = "raise",
    limit: Optional[int] = None,
) -> Optional[list[list[dict[str, Any]]]]:
    """Extract a table from an lxml element or tree using an xpath.

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract the table from.
        xpath (str): The xpath expression to select the table. Defaults to "//table".
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".

    Returns:
        Optional[list[dict[str, Any]]]: The list of extracted table rows, or None if no table found.

    Raises:
        NoElementsFoundError: If no table elements are found.
        NoXpathAttributesFoundError: If no xpath attributes are found.

    Examples:

        >>> from lxml import etree
        >>> html = '<table><tr><th>Name</th><th>Age</th></tr><tr><td>John</td><td>25</td></tr></table>'
        >>> tree = etree.ElementTree(etree.fromstring(html))
        >>> extract_tables(tree)
        [[{'Name': 'John', 'Age': '25'}]]

    """
    errors = OnError.from_any(errors)
    table_elements = extract_elements(tree, base_xpath, errors=errors)
    if not table_elements:
        if errors == OnError.RAISE:
            raise NoElementsFoundError
        return None
    tables_list = []
    for table_index in range(len(table_elements)):
        table_headers = extract_table_headers(
            tree,
            base_xpath + f"[{table_index}]//th/text()",
            errors=errors,
        )
        table_rows = extract_table_rows(
            tree,
            base_xpath + f"[{table_index}]//tbody/tr",
            errors=errors,
        )
        if not table_rows:
            if errors == OnError.RAISE:
                raise NoXpathAttributesFoundError
            return None

        if not table_headers:
            if has_headers and table_rows:
                table_headers = extract_table_headers(
                    tree, base_xpath + "//td/text()", errors=errors
                )
                if not table_headers:
                    if errors == OnError.RAISE:
                        raise NoXpathAttributesFoundError
                    return None
            else:
                if errors == OnError.RAISE:
                    raise NoXpathAttributesFoundError
                table_headers = [f"Column {i}" for i in range(len(table_rows[0]))]

        tables_list.append([dict(zip(table_headers, row)) for row in table_rows])

    limit = (
        len(tables_list)
        if (
            not limit
            or not is_numeric(limit)
            or (int_limit := int(float(limit))) <= 0
            or int_limit > len(tables_list)
        )
        else int(float(limit))
    )

    return tables_list[:limit]


def extract_table_headers(
    tree: Union[_Element, _ElementTree],
    xpath: str = "//table/thead/tr/th/text()",
    *,
    errors: Union[OnError, str] = "raise",
) -> Optional[list[str]]:
    """Extract table headers from an lxml element or tree using an xpath.

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract table headers from.
        xpath (str): The xpath expression to select the table headers. Defaults to "//table/thead/tr/th/text()".
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".

    Returns:
        Optional[list[str]]: The list of extracted table headers, or None if no table headers found.

    Raises:
        NoElementsFoundError: If no table headers are found.

    Examples:

        >>> from lxml import etree
        >>> html = '<table><thead><tr><th>Name</th><th>Age</th></tr></thead></table>'
        >>> tree = etree.ElementTree(etree.fromstring(html))
        >>> extract_table_headers(tree)
        ['Name', 'Age']

    """
    return extract_attributes(tree, xpath, errors=errors)


def extract_table_rows(
    tree: Union[_Element, _ElementTree],
    base_xpath: str = "//table/tbody/tr",
    *,
    errors: Union[OnError, str] = "raise",
) -> Optional[list[list[str]]]:
    """Extract table rows from an lxml element or tree using an xpath.

    Args:
        tree (Union[_Element, _ElementTree]): The lxml element or tree to extract table rows from.
        base_xpath (str): The xpath expression to select the table rows. Defaults to "//table/tbody/tr".
        errors (Union[OnError, str]): The error handling behavior. Defaults to "raise".

    Returns:
        Optional[list[list[str]]]: The list of extracted table rows, or None if no table rows found.

    Raises:
        NoElementsFoundError: If no table rows are found.

    Examples:

        >>> from lxml import etree
        >>> html = '<table><tr><td>John</td><td>25</td></tr><tr><td>Jane</td><td>30</td></tr></table>'
        >>> tree = etree.ElementTree(etree.fromstring(html))
        >>> extract_table_rows(tree)
        [['John', '25'], ['Jane', '30']]

    """
    errors = OnError.from_any(errors)
    table_rows = extract_elements(tree, base_xpath, errors=errors)
    if not table_rows:
        if errors == OnError.RAISE:
            raise NoElementsFoundError
        return None

    table_tds = [
        extract_attributes(row, base_xpath + "//td/text()", errors=errors)
        for row in table_rows
    ]

    return [x for x in table_tds if x]
