"""Logic blocks to be used when defining a daemon logic (loops, delays, ...)"""

from functools import wraps
from time import sleep
from typing import Any, Callable

from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


def forever_loop(
    catch_exceptions: bool = False,
    before_delay: float = 0.0,
    after_delay: float = 0.0,
) -> Callable:
    """
    Decorator to execute decorated function within a forever loop (while True:).
    It is useful when defining new custom daemons
    :param catch_exceptions: True to only display errors, False to raise them
    :type catch_exceptions: bool
    :param before_delay: Delay to wait (sleep) **before** a function execution has been completed
    :type before_delay: float
    :param after_delay: Delay to wait (sleep) **after** a function execution has been completed
    :type after_delay: float
    :return: Decorated function
    :rtype: Callable
    """

    def decorator(func: Callable) -> Callable:
        """
        Decorator
        :param func: Function to be decorated
        :type func: Callable
        :return: Function decorated
        :rtype: Callable
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            """
            Wrapper
            :param args: Positional arguments
            :type args: Any
            :param kwargs: Keyword arguments
            :type kwargs: Any
            :return: Nothing
            :rtype: None
            """
            while True:
                try:
                    if before_delay != 0.0:
                        sleep(before_delay)

                    # Running logic
                    func(*args, **kwargs)

                    if after_delay != 0.0:
                        sleep(after_delay)
                except Exception as exc_:
                    if catch_exceptions:
                        logger.error(f"Error: {exc_}")
                    else:
                        raise

        return wrapper

    return decorator
