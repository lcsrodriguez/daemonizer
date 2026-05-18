"""Utils to read environment variables"""

import os
from typing import Dict

from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


def get_env_vars() -> Dict[str, str]:
    """
    Function to read and returned environment variables
    :return: Dictionary of environment variables
    :rtype: Dict[str, str]
    """
    return dict(os.environ)


def get_env_var(var: str | None = None, default: str = "") -> str:
    """
    Function to read and return a single environment variable
    :param var: Environment variable to read
    :type var: str | None
    :param default: Default value to return if no environment variable exists
    :type default: str
    :return: Environment variable (string)
    :rtype: str
    """
    if var is None:
        return default
    return get_env_vars().get(var, default)
