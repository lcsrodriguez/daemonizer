"""Flags to be used in the daemon handler"""

from typing import List

START: int = 10
STOP: int = 20
RESTART: int = 30

STATUS: int = 40

FLAGS: List[int] = [START, STOP, RESTART, STATUS]
