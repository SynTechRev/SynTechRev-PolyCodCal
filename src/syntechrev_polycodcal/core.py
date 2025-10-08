"""Core utilities for SynTechRev-PolyCodCal.

This file contains a tiny example function used to verify packaging, testing,
and linting pipelines.
"""

from typing import Optional


def greet(name: Optional[str] = None) -> str:
    """Return a greeting message.

    Args:
        name: Optional name to include in the greeting. If None or empty,
            returns a generic greeting.

    Returns:
        A greeting string.
    """
    if not name:
        return "Hello, world!"
    return f"Hello, {name}!"
