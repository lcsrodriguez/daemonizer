"""Utils functions to check a given function body"""

import inspect
from enum import Enum
from typing import Any, Callable


def is_empty_function(func: Callable) -> bool:
    """
    Function to check if a function is empty.
    :param func: The function to check.
    :type func: Callable
    :return: True if the function is empty, False otherwise.
    :rtype: bool
    """
    return (
        len(
            [
                line
                for line in inspect.getsourcelines(func)[0]
                if line.strip()
                and not line.strip().startswith("#")
                and not line.strip().startswith('"""')
            ]
        )
        <= 1
    )


gv: Callable[[Enum], Any] = lambda e: e.value  # noqa: E731
