"""Context manager definition for modern daemon handler"""

from typing import List

from daemonizer.core.daemons.base import Daemon
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


class DaemonHandler:
    """
    Daemon handler class representing a context manager to be used in public API
    """

    def __init__(self) -> None:
        """
        Constructor func
        """
        self.daemons: List[Daemon] = []
        self.has_run: bool = False

    def __enter__(self) -> "DaemonHandler":
        """
        Context manager entry point
        :return: Current object
        :rtype: DaemonHandler
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Context manager exit point
        :return: Nothing
        :rtype: None
        """
        self.run()

    def run(self) -> None:
        """
        Function to run the daemon handler logic
        :return: Nothing
        :rtype: None
        """
        if not self.has_run:
            self.has_run = True

            # TODO: Adding handler part here for each registered daemons
            print(self.daemons)

    def add(self, daemon: Daemon) -> None:
        """
        Function to register a new daemon to the handler
        :param daemon: Daemon object to be registered
        :type daemon: Daemon
        :return: Nothing
        :rtype: None
        """
        if issubclass(daemon.__class__, Daemon):  # isinstance(other, Daemon):
            self.daemons.append(daemon)
