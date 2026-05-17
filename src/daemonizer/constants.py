"""List of defined constants to be used in the project"""

from importlib.metadata import PackageNotFoundError, version
from typing import List, Tuple

APP_NAME: str = "daemonizer"

PKG_NAME: str = f"{APP_NAME}-py"

# Version dynamically updated via Makefile targets
APP_VERSION: str = version(PKG_NAME)
APP_VERSION_TUPLE: Tuple[int, ...] = tuple(map(int, APP_VERSION.split(".")))

try:
    __version__: str = version(PKG_NAME)
except PackageNotFoundError:
    __version__ = "unknown"  # "0.0.0"


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

DEFAULT_PID_FILENAME_LENGTH: int = 5

# Start method to be used when creating child processes from `multiprocessing` module
MULTIPROC_START_METHOD: str = "fork"
