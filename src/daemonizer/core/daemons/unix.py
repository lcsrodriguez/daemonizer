"""UNIX daemon implementation"""

import atexit
import logging
import os
import signal
import sys
import time
from typing import Any, Dict, Tuple

from daemonizer.core.daemons.base import Daemon
from daemonizer.core.pid.pidfile import Pidfile
from daemonizer.files import DAEMONIZER_BASE_DIR
from daemonizer.utils.func import is_empty_function
from daemonizer.utils.logs import get_logger
from daemonizer.utils.process import is_active_process
from daemonizer.utils.streams import log_err, log_out, stream_err, stream_in, stream_out

logger = get_logger(__name__)

# Frame = type("Frame", (), {})


class UNIXDaemon(Daemon):
    """
    UNIX daemon
    Base class to define a valid daemon logic to be run on UNIX distributions
    To define a UNIX daemon, you must override `UNIXDaemon.run(...)` abstract method
    """

    """
    __slots__: Tuple[str, ...] = (
        "pidfile",
        "daemon_name",
        "daemon_pid",
        "is_alive",
        "working_directory",
        "umask",
        "logger",
    )
    """

    def __init__(
        self,
        name: str = "",
        pidfile: Pidfile | None = None,
        working_directory: str = "/",
        umask: int = 0,  # 0o022
        dlogger: logging.Logger | None = None,
        stop_daemon_signal: int = signal.SIGTERM,
        *args,
        **kwargs,
    ) -> None:
        """
        Daemon constructor function
        :param name: Daemon name
        :type name: str
        :param pidfile: PID file
        :type pidfile: Pidfile
        :param working_directory: Working directory for daemon
        :type working_directory: str
        :param umask: umask
        :type umask: int
        :param dlogger: Daemon logger
        :type dlogger: logging.Logger
        :param args: Positional arguments
        :type args: Tuple[Any, ...]
        :param kwargs: Keyword arguments
        :type kwargs: Dict[str, Any]
        """

        # Daemon name
        self.daemon_name: str = name if name != "" else "unix_daemon"

        if pidfile is None:
            pidfile = Pidfile(
                pid_name=self.daemon_name,
            )
            self.pidfile: Pidfile = pidfile
        else:
            if isinstance(pidfile, Pidfile):
                self.pidfile = pidfile

        # Daemon PID
        self.daemon_pid: int = 0

        # Signal to be used to stop the daemon (:= kill the process)
        self.stop_daemon_signal: int = stop_daemon_signal

        # Daemon working directory
        self.working_directory: str = working_directory

        # Daemon umask
        self.umask: int = umask

        # Handling input logger
        self.logger: logging.Logger = (
            dlogger
            if dlogger is not None and isinstance(dlogger, logging.Logger)
            else logging.getLogger(__name__)
        )

        # Arguments
        self.daemon_args: Dict[str, Tuple[Any, ...] | Dict[str, Any]] = {
            "args": args,
            "kwargs": kwargs,
        }

        # Flag to track whether current daemon is alive
        self.is_alive: bool = False

    def get_arguments(self) -> Dict[str, Tuple[Any, ...] | Dict[str, Any]]:
        """
        Function to get arguments
        This method can be called in the custom daemon logic
        :return: Dict of both positional and keyword arguments
        :rtype: Dict[str, Tuple[Any, ...] | Dict[str, Any]]
        """
        return self.daemon_args

    def args(self) -> Tuple[Any, ...]:
        """
        Function to access positional arguments (defined at daemon definition)
        from daemon's body
        :return: Positional arguments
        :rtype: Tuple[Any, ...]
        """
        return self.daemon_args.get("args", ())  # type: ignore[union-attr, return-value]

    def kwargs(self) -> Dict[str, Any]:
        """
        Function to access keyword arguments (defined at daemon definition)
        from daemon's body
        :return: Keyword arguments
        :rtype: Dict[str, Any]
        """
        return self.daemon_args.get("kwargs", {})  # type: ignore[union-attr, return-value]

    def _deleting_pidfile(self) -> None:
        """
        Function to clean-delete associated PID file
        :return: Nothing
        :rtype: None
        """
        if self.pidfile.is_existing_file():
            self.pidfile.delete()
            log_out(f"Pidfile (file={self.pidfile.abs_path}) deleted\n")

    def stop(self) -> None:
        """
        Function to stop the daemon.
            - If the PID file is on the disk (same name as current daemon), we read the PID in the file
                - If process (identified by PID) is still active, we kill it with specified signal (`self.stop_daemon_signal`)
                - If process is not active anymore (it may have been terminated by natural cause (core logic) or external
                signal sent by the user), we are removing PID file (not needed anymore)
            - If the PID file is not on the disk, we cannot stop the daemon.
        This is why it is important to avoid manipulating PID files as their management is handled automatically by the
        library.
        :return: Nothing
        :rtype: None
        """
        if not self.pidfile.is_existing_file():
            log_err(
                f"Pidfile (file={self.pidfile.abs_path}) does not exist. Daemon not running?\n"
            )
            return None

        # Reading PID
        pid_: int = self.pidfile.read()

        # Checking if the process is still alive
        if not is_active_process(pid_=pid_):
            log_err(
                "This daemon is currently not running on this machine. No stop needed"
            )
            self._deleting_pidfile()
            sys.exit(1)

        try:
            while True:
                os.kill(pid_, self.stop_daemon_signal)  # signal.SIGTERM
                log_out(f"Daemon {self.daemon_name} stopped\n")
                time.sleep(0.1)
                self.is_alive = False
                # TODO: Check if the process is still alive to break
        except OSError as exc_:
            exc_args = str(exc_.args)
            if exc_args.find("No such process") > 0:
                self._deleting_pidfile()
            else:
                print(exc_args)
                sys.exit(1)

    def start(self) -> None:
        """
        Function to start the daemon
        :return: Nothing
        :rtype: None
        """

        # Check if the pidfile already exists
        if self.pidfile.is_existing_file():
            log_err(
                f"Pidfile (file={self.pidfile.abs_path}) already exists.Daemon already running?\n"
            )
            sys.exit(1)

        if not self._check_valid_core_logic():
            log_err(
                "The core logic of the daemon is invalid. Please override the run method\n"
            )
            sys.exit(1)

        # Start the daemonization process
        self._daemonize()
        self.run()

    def restart(self) -> None:
        """
        Function to restart the daemon (it stops then starts the process)
        Once restarted, daemon has a new PID (new process)
        :return: Nothing
        :rtype: None
        """
        self.stop()
        # TODO: If stops fails (no running daemon), do not start !!

        self.start()

    def status(self):
        """
        Function to get status of the current daemon
        :return: Nothing
        :rtype: None
        """
        if self._status():
            log_out(
                f"Daemon {self.daemon_name} is running with PID {self.pidfile.read()}"
            )
        else:
            log_out(f"Daemon {self.daemon_name} is not running")

    def _status(self) -> bool:
        """
        Function to get current daemon status (process active or not)
        :return: True if daemon process is active, False otherwise
        :rtype: bool
        """
        try:
            pid: int = self.pidfile.read()

            if is_active_process(pid_=pid):
                return True
        except Exception as exc_:
            logger.warning(f"An error has occurred while trying to read PID: {exc_}")
            return False
        return False

    def run(self) -> None:
        """
        Method to run the daemon.
        This method must be overridden by the child class.
        :return: Nothing
        :rtype: None
        """
        ...
        # raise NotImplementedError()

    def _daemonize(self) -> None:
        """
        Daemonize the process by applying the UNIX double fork method.
        This private method ensures the daemon logic (defined and executed in the `.run(...)` method)
        will be executed in a totally-independent process (detached from other running processes) and be run in
        :return: Nothing
        :rtype: None
        """
        logger.info("Daemonizing process...")

        # Perform first fork
        try:
            _pid = os.fork()
            if _pid > 0:  # Exit first parent
                sys.exit(0)
        except OSError as exc_:
            stream_err().write(f"Fork 1 has failed: {exc_.errno}({exc_.strerror})\n")
            sys.exit(1)

        # Decouple first child from parent process environment
        os.chdir(self.working_directory)
        os.setsid()
        os.umask(self.umask)

        # Perform second fork
        try:
            _pid = os.fork()
            if _pid > 0:  # Exit second parent
                sys.exit(0)
        except OSError as exc_:
            stream_err().write(f"Fork 2 has failed: {exc_.errno}({exc_.strerror})\n")
            sys.exit(1)

        # Flushing streams buffers to avoid any data loss
        stream_out().flush()
        stream_err().flush()

        # Redirect standard file descriptors
        stream_i = open(os.devnull, "r")
        stream_o = open(os.devnull, "a+")
        stream_e = open(os.devnull, "a+")

        os.dup2(stream_i.fileno(), stream_in().fileno())
        os.dup2(stream_o.fileno(), stream_out().fileno())
        os.dup2(stream_e.fileno(), stream_err().fileno())

        # Get damon PID
        self.daemon_pid = os.getpid()

        # Write the pidfile on-disk
        self.pidfile.write(self.daemon_pid)

        # Adding signal handlers
        self._graceful_signal_handler()

        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGHUP, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGQUIT, self._signal_handler)
        # signal.signal(signal.SIGKILL, self._signal_handler)  # Cannot be caught, blocked, or ignored
        # __ = list(map(lambda sn: signal.signal(sn, handler=self._signal_handler), [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]))

        self.is_alive = True

    def _signal_handler(self, signum: int, frame):
        """
        Signal handler method to register callback func to be executed once we catch a signal sent to daemon
        :param signum: Signal number
        :type signum: int
        :param frame: Frame object
        :type frame: Frame
        :return: Nothing
        :rtype: None
        """

        # self.pidfile.delete()
        self._deleting_pidfile()

        self.is_alive = False
        with open(DAEMONIZER_BASE_DIR / "events.log", "a") as f:
            f.write(f"Signal {signum} received\n")
        sys.exit(0)  # Exiting the process

    def _graceful_signal_handler(self) -> None:
        """
        Graceful signal handler method.
        :return: Nothing
        :rtype: None
        """
        atexit.register(self.pidfile.delete)
        atexit.register(self._deleting_pidfile)

    def _check_valid_core_logic(self) -> bool:
        """
        Method to check if the core logic of the daemon is valid.
        :return:
        :rtype:
        """
        return not is_empty_function(func=self.run)


# Class aliases
# LinuxDaemon = UNIXDaemon
# MacOSDaemon = UNIXDaemon
