"""Base daemon"""

from abc import ABC, abstractmethod
from multiprocessing.synchronize import Lock as LockType
from types import FrameType
from typing import Tuple

# Add possibility to run logic block **BEFORE** the daemonization and fail if raise for ex


class Daemon(ABC):
    """
    Class **Daemon**

    Daemon base class to be inherited by other classes
    """

    __slots__: Tuple[str, ...] = ("daemon_name",)

    @abstractmethod
    def start(self) -> None:
        """
        Function to start a daemon
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def stop(self):
        """
        Function to stop a daemon
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def restart(self):
        """
        Function to restart a daemon
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def status(self):
        """
        Function to get status of daemon
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def run(self):
        """
        Function to run a daemon
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def _daemonize(self):
        """
        Function to daemonize a specific logic
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def _signal_handler(self, signum: int, frame: FrameType) -> None:
        """
        Function to stop a daemon
        :param signum: signal number
        :type signum: int
        :param frame: Frame
        :type frame: FrameType
        :return: Nothing
        :rtype: None
        """
        ...

    @abstractmethod
    def set_lock(self, lock: LockType | None) -> None:
        """
        Function to set lock for PID file writes
        :param lock: Multiprocessing lock to protect PID file on-disk writes
        :type lock: LockType | None
        :return: Nothing
        :rtype: None
        """
        ...
