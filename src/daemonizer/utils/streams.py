"""Utils func to interact with streams (stdin, stdout, stderr)"""

import sys
from typing import TextIO


def stream_in() -> TextIO:
    """
    Function to get stream stdin
    :return: Stream stdin
    :rtype: TextIO
    """
    return sys.stdin


def stream_out() -> TextIO:
    """
    Function to get stream stdout
    :return: Stream stdout
    :rtype: TextIO
    """
    return sys.stdout


def stream_err() -> TextIO:
    """
    Function to get stream stderr
    :return: Stream stderr
    :rtype: TextIO
    """
    return sys.stderr


def log_in(msg: str = "") -> None:
    """
    Function to log on stdin
    :param msg: Message to log
    :type msg: str
    :return: Nothing
    :rtype: None
    """
    stream_in().write(f"{msg}\n")


def log_out(msg: str = "") -> None:
    """
    Function to log on stdout
    :param msg: Message to log
    :type msg: str
    :return: Nothing
    :rtype: None
    """
    stream_out().write(f"{msg}\n")


def log_err(msg: str = "") -> None:
    """
    Function to log on stderr
    :param msg: Message to log
    :type msg: str
    :return: Nothing
    :rtype: None
    """
    stream_err().write(f"{msg}\n")
