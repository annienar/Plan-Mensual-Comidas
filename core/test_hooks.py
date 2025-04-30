"""Module for testing pre-commit hooks functionality."""

from typing import Any, Dict, List


def test_function(param1: Any, param2: str) -> None:
    """Format a key-value pair into a dictionary.

    Args:
        param1: First parameter of any type
        param2: Second parameter as string
    """
    data: Dict[str, Any] = {"key1": param1, "key2": param2}
    print(data)


def another_function() -> List[Any]:
    """Return an empty list for testing purposes.

    Returns:
        An empty list
    """
    empty_list: List[Any] = []
    return empty_list
