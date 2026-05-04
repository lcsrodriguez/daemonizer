"""List of defined constants to be used in the project"""

from importlib.metadata import version
from typing import List, Tuple

APP_NAME: str = "daemonizer"

# Version dynamically updated via Makefile targets
APP_VERSION: str = version(APP_NAME)
APP_VERSION_TUPLE: Tuple[int, ...] = tuple(map(int, APP_VERSION.split(".")))


# UNIX system names
UNIX_SYSTEM_NAMES: List[str] = [
    "Linux",
    "Darwin",
    "FreeBSD",
    "NetBSD",
    "OpenBSD",
    "SunOS",
    "AIX",
]
