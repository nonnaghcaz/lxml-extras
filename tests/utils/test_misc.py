"""Tests for the lxml_extras.utils.misc module."""

from lxml_extras.utils.misc import is_numeric


def test_is_numeric() -> None:
    """Test is_numeric."""
    assert is_numeric(1)
    assert is_numeric(1.0)
    assert is_numeric("1")
    assert is_numeric("1.0")
    assert is_numeric("1e0")
    assert is_numeric("1e-0")
    assert is_numeric("1e+0")
    assert is_numeric("1.0e0")
    assert is_numeric("1.0e-0")
    assert is_numeric("1.0e+0")
    assert is_numeric("1.0e1")
    assert is_numeric("1.0e-1")
    assert is_numeric("1.0e+1")
    assert is_numeric("1.0e01")
    assert is_numeric("1.0e-01")
    assert is_numeric("1.0e+01")

    assert not is_numeric("a")
    assert not is_numeric("1a")
    assert not is_numeric("1.0a")
    assert not is_numeric("1ea")
    assert not is_numeric("1e-a")
    assert not is_numeric("1e+a")
    assert not is_numeric("1.0ea")
    assert not is_numeric("1.0e-a")
    assert not is_numeric("1.0e+a")
