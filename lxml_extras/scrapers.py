"""Scraping utilities using lxml and requests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from lxml_extras.extractors import extract_images, extract_links
from lxml_extras.utils.enums import OnError

if TYPE_CHECKING:
    from collections.abc import Mapping  # pragma: no cover

    from lxml.etree import _ElementTree

from io import BytesIO

import requests
from lxml import etree


def get_tree(
    url: str,
    *,
    params: Optional[Mapping[str, str]] = None,
    headers: Optional[dict] = None,
    timeout: int = 60,
) -> _ElementTree:
    """Get the HTML tree from a URL using requests."""
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    parser = etree.HTMLParser()
    return etree.parse(BytesIO(response.content), parser)  # noqa: S320


def scrape_images(
    url: str,
    xpath: str = "//img/@src",
    *,
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Scrape images from a URL using an xpath."""
    return extract_images(
        get_tree(url),
        xpath=xpath,
        default=default,
        errors=errors,
        limit=limit,
    )


def scrape_first_image(
    url: str,
    xpath: str = "//img/@src",
    *,
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
) -> Optional[str]:
    """Scrape the first image from a URL using an xpath."""
    if not (
        images := scrape_images(
            url,
            xpath=xpath,
            default=default,
            errors=errors,
            limit=1,
        )
    ):
        return default
    return images[0]


def scrape_links(
    url: str,
    xpath: str = "//a/@href",
    *,
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
    limit: Optional[int] = None,
) -> Optional[list[str]]:
    """Scrape links from a URL using an xpath."""
    return extract_links(
        get_tree(url),
        xpath=xpath,
        default=default,
        errors=errors,
        limit=limit,
    )


def scrape_first_link(
    url: str,
    xpath: str = "//a/@href",
    *,
    default: Optional[str] = None,
    errors: OnError = OnError.RAISE,
) -> Optional[str]:
    """Scrape the first link from a URL using an xpath."""
    links = scrape_links(url, xpath=xpath, default=default, errors=errors, limit=1)
    if not links:
        return default
    return links[0]
