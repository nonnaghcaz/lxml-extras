"""Tests for the lxml_extras.utils.enums module."""

import pytest

from lxml_extras.utils.enums import OnError
from lxml_extras.utils.exceptions import InvalidOnErrorValueError


def test_from_str() -> None:
    """Test from_str."""
    assert OnError.from_str("raise") == OnError.RAISE
    assert OnError.from_str("ignore") == OnError.IGNORE
    with pytest.raises(InvalidOnErrorValueError):
        OnError.from_str("invalid")


def test_to_str() -> None:
    """Test to_str."""
    assert OnError.RAISE.to_str() == "raise"
    assert OnError.IGNORE.to_str() == "ignore"


def test_from_any() -> None:
    """Test from_any."""
    assert OnError.from_any("raise") == OnError.RAISE
    assert OnError.from_any("ignore") == OnError.IGNORE
    assert OnError.from_any(OnError.RAISE) == OnError.RAISE
    assert OnError.from_any(OnError.IGNORE) == OnError.IGNORE
    with pytest.raises(InvalidOnErrorValueError):
        OnError.from_any("invalid")
