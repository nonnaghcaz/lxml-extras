from lxml.etree import _Element, _ElementTree

from lxml_extras.utils.enums import OnError as OnError
from lxml_extras.utils.exceptions import (
    InvalidXpathAttributeError as InvalidXpathAttributeError,
)
from lxml_extras.utils.exceptions import InvalidXpathError as InvalidXpathError
from lxml_extras.utils.exceptions import (
    NoXpathAttributesFoundError as NoXpathAttributesFoundError,
)
from lxml_extras.utils.exceptions import XpathTooShortError as XpathTooShortError
from lxml_extras.utils.misc import is_numeric as is_numeric

def extract_attributes(
    tree: _Element | _ElementTree,
    xpath: str,
    *,
    errors: OnError | str = "raise",
    limit: int | None = None,
) -> list[str] | None: ...
def extract_links(
    tree: _Element | _ElementTree,
    xpath: str = "//a/@href",
    *,
    errors: OnError | str = "raise",
    limit: int | None = None,
) -> list[str] | None: ...
def extract_images(
    tree: _Element | _ElementTree,
    xpath: str = "//img/@src",
    *,
    errors: OnError | str = "raise",
    limit: int | None = None,
) -> list[str] | None: ...
def extract_first_image(
    tree: _Element | _ElementTree,
    xpath: str = "//img/@src",
    *,
    errors: OnError | str = "raise",
) -> str | None: ...
