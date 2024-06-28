"""Enums for lxml_extras."""

from __future__ import annotations

from enum import Enum

from lxml_extras.utils.exceptions import InvalidOnErrorValueError


class OnError(Enum):
    """Error handling options."""

    RAISE = 1
    IGNORE = 2

    @classmethod
    def from_str(cls, value: str) -> OnError:
        """Convert a string to an OnError enum."""
        try:
            return cls[value.upper()]
        except KeyError as ex:
            raise InvalidOnErrorValueError from ex

    def to_str(self) -> str:
        """Convert an OnError enum to a string."""
        return self.name.lower()

    @classmethod
    def from_any(cls, value: str | OnError) -> OnError:
        """Convert a string or OnError enum to an OnError enum."""
        return cls.from_str(value) if isinstance(value, str) else value
