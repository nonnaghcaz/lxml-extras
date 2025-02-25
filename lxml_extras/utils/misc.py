"""Miscellaneous utility functions."""


def is_numeric(value: str) -> bool:
    """Check if a value is numeric."""
    try:
        int(float(value))
    except ValueError:
        return False
    return True
