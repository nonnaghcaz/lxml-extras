"""Enums for lxml_extras."""

from enum import Enum


class OnError(Enum):
    """Error handling options."""

    RAISE = 1
    IGNORE = 2
