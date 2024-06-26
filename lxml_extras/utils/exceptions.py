"""Custom exceptions for the lxml_extras package."""

from __future__ import annotations


class XpathTooShortError(ValueError):
    """Raised when an xpath is too short."""

    def __init__(
        self: XpathTooShortError,
        message: str = "Invalid xpath: must have at least two valid parts",
    ) -> None:
        """Initialize the exception."""
        super().__init__(message)


class InvalidXpathAttributeError(ValueError):
    """Raised when an attribute is invalid."""

    def __init__(
        self: InvalidXpathAttributeError,
        message: str = "Invalid xpath: attribute must be text() or @attribute",
    ) -> None:
        """Initialize the exception."""
        super().__init__(message)


class NoXpathAttributesfoundError(ValueError):
    """Raised when no attributes are found."""

    def __init__(
        self: NoXpathAttributesfoundError,
        message: str = "No attributes found",
    ) -> None:
        """Initialize the exception."""
        super().__init__(message)


class InvalidXpathError(ValueError):
    """Raised when an xpath is invalid."""

    def __init__(
        self: InvalidXpathError,
        message: str = "Invalid xpath",
    ) -> None:
        """Initialize the exception."""
        super().__init__(message)


class StringifyError(ValueError):
    """Raised when an object cannot be stringified."""

    def __init__(
        self: StringifyError,
        message: str = "Cannot stringify object",
    ) -> None:
        """Initialize the exception."""
        super().__init__(message)
