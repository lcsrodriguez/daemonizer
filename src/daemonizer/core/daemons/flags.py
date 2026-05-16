"""Flags to be used in the daemon handler"""

from typing import List

START: int = 10
STOP: int = 20
RESTART: int = 30

STATUS: int = 40

FLAGS: List[int] = [START, STOP, RESTART, STATUS]

# Default flag (we set it to STATUS as it is an idempotent operation, and it is not modifying the daemon's status)
DEFAULT_FLAG: int = STATUS
