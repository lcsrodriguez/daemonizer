"""Context manager definition for modern daemon handler"""

from typing import List

from daemonizer.core.daemons.base import Daemon
from daemonizer.core.daemons.flags import FLAGS, RESTART, START, STATUS, STOP
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
            logger.info("Running handler")

            # TODO: Adding handler part here for each registered daemons
            self.perform(flags=[START])

    def perform(self, flags: List[int] | int | None = None) -> None:
        """
        Function to perform operations on currently-registered daemons.
        This function handles START, STOP, RESTART and STATUS flags (defined in `core.daemons.flags`)
        :param flags: Flags to be performed on currently registered daemons
        :type flags: List[int] | int | None
        :return: Nothing
        :rtype: None
        """
        if flags is None:
            logger.warning("No flags provided")
            return

        if isinstance(flags, int):
            flags = [flags]

        for flag in flags:
            if flag not in FLAGS:
                logger.warning(f"Current flag {flag} not supported")
                continue

            for daemon in self.daemons:
                if flag == START:
                    daemon.start()
                elif flag == STOP:
                    daemon.stop()
                elif flag == RESTART:
                    daemon.restart()
                elif flag == STATUS:
                    daemon.status()

        # Cleaning daemons
        self.daemons.clear()

    def add(self, daemon: Daemon) -> None:
        """
        Function to register a new daemon to the handler
        :param daemon: Daemon object to be registered
        :type daemon: Daemon
        :return: Nothing
        :rtype: None
        """
        if issubclass(daemon.__class__, Daemon):  # isinstance(other, Daemon):
            logger.info(f"Registering new daemon {daemon}")
            self.daemons.append(daemon)
