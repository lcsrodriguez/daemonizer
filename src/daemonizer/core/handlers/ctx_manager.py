"""Context manager definition for modern daemon handler"""

from multiprocessing import Lock, Process, set_start_method
from multiprocessing.synchronize import Lock as LockType
from typing import Dict, List, Set, Tuple, Type

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
        self.daemon_requests: List[Tuple[Daemon, int]] = []
        self.has_run: bool = False

        # Set of daemon classes (types) from the daemon registered by the user
        # We keep this information as we are setting up a multiproc `Lock` for each type of daemon
        self.daemon_types: Set[Type] = set()

        # Storing daemon locks (daemon type -> Lock)
        self.daemon_op_locks: Dict[Type, LockType] = {}

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

            self.perform()

    # TODO: Multiprocessing for each handler
    @staticmethod
    def _perform_op_on_daemon(
        daemon: Daemon | None = None,
        flag: int | None = None,
        lock: LockType | None = None,
    ) -> None:
        """
        Function to perform an operation on a given daemon
        :param daemon: Input daemon
        :type daemon: Daemon | None
        :param flag: Flag of operation to be performed on given daemon
        :type flag: int | None
        :param lock: Lock from the input daemon type
        :type lock: LockType | None
        :return: Nothing
        :rtype: None
        """

        if daemon is None:
            logger.error("No daemon provided")
            return

        if flag is None:
            logger.error("Invalid input flag")
            return

        # Setting up lock to underlying daemon to protect PID file writing
        daemon.set_lock(lock=lock)

        # Applying operation to given
        if flag == START:
            daemon.start()
        elif flag == STOP:
            daemon.stop()
        elif flag == RESTART:
            daemon.restart()
        elif flag == STATUS:
            daemon.status()

    def perform(self) -> None:
        """
        Function to perform operations on currently-registered daemon requests.
        This function handles START, STOP, RESTART and STATUS flags (defined in `core.daemons.flags`)
        :return: Nothing
        :rtype: None
        """

        # Issuing
        for daemon_type in self.daemon_types:
            self.daemon_op_locks[daemon_type] = Lock()

        processes: List[Process] = []
        # Processing each request
        for daemon, flag in self.daemon_requests:
            lock = self.daemon_op_locks.get(daemon.__class__, None)
            if lock is None:
                logger.warning(
                    f"No lock for this type of daemon: {daemon.__class__.__name__}"
                )

            p = Process(target=self._perform_op_on_daemon, args=(daemon, flag, lock))
            # self._perform_op_on_daemon(daemon=daemon, flag=flag)
            processes.append(p)

        # Starting processes
        for p in processes:
            p.start()

        # Joining (waiting for termination) processes
        for p in processes:
            p.join()

        # Cleaning daemons
        self.daemon_requests.clear()

    def _add_request(
        self, daemon: Daemon | None = None, flag: int | None = None
    ) -> None:
        """
        Function to add a request to the daemon
        :param daemon: Input daemon
        :type daemon: Daemon | None
        :param flag: Flag operation to be performed on given daemon
        :type flag: int | None
        :return: Nothing
        :rtype: None
        """

        if daemon is None:
            logger.error("No daemon provided")
            return

        if not issubclass(daemon.__class__, Daemon):  # isinstance(other, Daemon):
            logger.error("Invalid input daemon")
            return

        if flag is None:
            logger.error("Invalid input flag")
            return

        if flag not in FLAGS:
            logger.error(f"Current flag {flag} not supported")
            return

        # logger.info(f"Registering new request for daemon: {daemon} (operation: {flag})")
        # Adding daemon type to set
        self.daemon_types.add(daemon.__class__)

        # Adding operation on daemon request
        self.daemon_requests.append((daemon, flag))

    def start(self, daemon: Daemon | None = None) -> "DaemonHandler":
        """
        Function to add a request to start input daemon
        :param daemon: Daemon
        :type daemon: Daemon | None
        :return: Self object
        :rtype: DaemonHandler
        """
        self._add_request(daemon, START)
        return self

    def stop(self, daemon: Daemon | None = None) -> "DaemonHandler":
        """
        Function to add a request to stop input daemon
        :param daemon: Daemon
        :type daemon: Daemon | None
        :return: Self object
        :rtype: DaemonHandler
        """
        self._add_request(daemon, STOP)
        return self

    def status(self, daemon: Daemon | None = None) -> "DaemonHandler":
        """
        Function to add a request to get status from input daemon
        :param daemon: Daemon
        :type daemon: Daemon | None
        :return: Self object
        :rtype: DaemonHandler
        """
        self._add_request(daemon, STATUS)
        return self

    def restart(self, daemon: Daemon | None = None) -> "DaemonHandler":
        """
        Function to add a request to restart input daemon
        :param daemon: Daemon
        :type daemon: Daemon | None
        :return: Self object
        :rtype: DaemonHandler
        """
        self._add_request(daemon, RESTART)
        return self
