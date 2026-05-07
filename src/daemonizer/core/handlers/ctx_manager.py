"""Context manager definition for modern daemon handler"""

from multiprocessing import Process, set_start_method
from typing import List

from daemonizer.constants import MULTIPROC_START_METHOD
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
        # Setting new process start method to fork
        # docs: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_start_method
        # docs: https://docs.python.org/3/library/multiprocessing.html#multiprocessing-start-methods
        try:
            set_start_method(method=MULTIPROC_START_METHOD)
        except RuntimeError as exc_:
            logger.warning(
                f"Multiprocessing start method has already been set previously (error: {exc_})"
            )
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

    # TODO: Multiprocessing for each handler
    @staticmethod
    def _perform_op_on_daemon(
        daemon: Daemon | None = None, flag: int | None = None
    ) -> None:
        """
        Function to perform an operation on a given daemon
        :param daemon: Input daemon
        :type daemon: Daemon | None
        :param flag: Flag of operation to be performed on given daemon
        :type flag: int | None
        :return: Nothing
        :rtype: None
        """

        # TODO: to be used in perform(...)
        if daemon is None:
            logger.error("No daemon provided")
            return

        if not issubclass(daemon.__class__, Daemon):
            logger.error("Invalid input daemon")
            return

        if flag is None:
            logger.error("Invalid input flag")
            return

        if flag not in FLAGS:
            logger.error(f"Current flag {flag} not supported")
            return

        # Applying operation to given
        if flag == START:
            daemon.start()
        elif flag == STOP:
            daemon.stop()
        elif flag == RESTART:
            daemon.restart()
        elif flag == STATUS:
            daemon.status()

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
            processes: List[Process] = []
            for daemon in self.daemons:
                p = Process(target=self._perform_op_on_daemon, args=(daemon, flag))
                # self._perform_op_on_daemon(daemon=daemon, flag=flag)
                processes.append(p)

            # Starting processes
            for p in processes:
                p.start()

            # Joining (waiting for termination) processes
            for p in processes:
                p.join()

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
