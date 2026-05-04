"""UNIX daemon"""

import atexit
import logging
import os
import signal
import sys
import time
from enum import Enum
from typing import Any, Dict, Tuple

from daemonizer.core.daemons.base import Daemon
from daemonizer.core.pid.pidfile import Pidfile

# from daemonizer.exceptions import InvalidPIDFileError
from daemonizer.utils.func import gv, is_empty_function
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)

# Frame = type("Frame", (), {})


class StandardStreams(Enum):
    """Enum to store the standard streams"""

    IN = sys.stdin
    OUT = sys.stdout
    ERR = sys.stderr


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
        *args: Tuple[Any, ...],
        **kwargs: Dict[str, Any],
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

    def stop(self) -> None:
        """
        Function to stop the daemon
        :return: Nothing
        :rtype: None
        """
        if not self.pidfile.is_existing_file():
            gv(StandardStreams.ERR).write(
                f"Pidfile (file={self.pidfile.abs_path}) does not exist. Daemon not running?\n"
            )
            return

        pid_: int = self.pidfile.read()

        try:
            while True:
                os.kill(pid_, signal.SIGTERM)
                gv(StandardStreams.OUT).write(f"Daemon {self.daemon_name} stopped\n")
                time.sleep(0.1)
                self.is_alive = False
                # TODO: Check if the process is still alive to break
        except OSError as exc_:
            exc_args = str(exc_.args)
            if exc_args.find("No such process") > 0:
                if self.pidfile.is_existing_file():
                    self.pidfile.delete()
                    gv(StandardStreams.OUT).write(
                        f"Pidfile (file={self.pidfile.abs_path}) deleted\n"
                    )
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
            gv(StandardStreams.ERR).write(
                f"Pidfile (file={self.pidfile.abs_path}) already exists.Daemon already running?\n"
            )
            sys.exit(1)

        if not self._check_valid_core_logic():
            gv(StandardStreams.ERR).write(
                "The core logic of the daemon is invalid. Please override the run method\n"
            )
            sys.exit(1)

        # Start the daemonization process
        self.daemonize()
        self.run()

    def restart(self) -> None:
        """
        Function to restart the daemon
        Once restarted, daemon has a new PID (new process)
        :return: Nothing
        :rtype: None
        """
        self.stop()
        # TODO: If stops fails (no running daemon), do not start !!

        self.start()

    def status(self):
        """
        Function to get status
        :return: Nothing
        :rtype: None
        """
        gv(StandardStreams.OUT).write(
            f"Daemon {self.daemon_name} is running with pid {self.pidfile.read()}\n"
        )

    def run(self) -> None:
        """
        Method to run the daemon.
        This method must be overridden by the child class.
        :return: Nothing
        :rtype: None
        """
        ...

    def daemonize(self) -> None:
        """
        Daemonize the process by applying the UNIX double fork method.
        :return: Nothing
        :rtype: None
        """
        print("daemonize")
        # Perform first fork

        try:
            _pid = os.fork()
            if _pid > 0:  # Exit first parent
                sys.exit(0)
        except OSError as exc_:
            sys.stderr.write(f"Fork 1 has failed: {exc_.errno}({exc_.strerror})\n")
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
            sys.stderr.write(f"Fork 1 has failed: {exc_.errno}({exc_.strerror})\n")
            sys.exit(1)

        # Flushing streams buffers to avoid any data loss
        gv(StandardStreams.OUT).flush()
        gv(StandardStreams.ERR).flush()

        # Redirect standard file descriptors
        stream_i = open(os.devnull, "r")
        stream_o = open(os.devnull, "a+")
        stream_e = open(os.devnull, "a+")

        os.dup2(stream_i.fileno(), gv(StandardStreams.IN).fileno())
        os.dup2(stream_o.fileno(), gv(StandardStreams.OUT).fileno())
        os.dup2(stream_e.fileno(), gv(StandardStreams.ERR).fileno())

        self.daemon_pid = os.getpid()

        # Write the pidfile on-disk
        self.pidfile.write(self.daemon_pid)

        self._graceful_signal_handler()

        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGHUP, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGQUIT, self._signal_handler)
        # signal.signal(signal.SIGKILL, self._signal_handler)  # Cannot be caught, blocked, or ignored
        # __ = list(map(lambda sn: signal.signal(sn, handler=self._signal_handler), [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]))

        self.is_alive = True

    def _signal_handler(self, signum, frame):
        # """
        # Signal handler method.
        # :param signum: Signal number
        # :type signum: int
        # :param frame: Frame object
        # :type frame: Frame
        # :return: Nothing
        # :rtype: None
        # """

        self.pidfile.delete()
        self.is_alive = False
        with open("/tmp/events.log", "a") as f:
            f.write(f"Signal {signum} received\n")
        sys.exit(0)  # Exiting the process

    def _graceful_signal_handler(self) -> None:
        """
        Graceful signal handler method.
        :return: Nothing
        :rtype: None
        """
        atexit.register(self.pidfile.delete)

    def _check_valid_core_logic(self) -> bool:
        """
        Method to check if the core logic of the daemon is valid.
        :return:
        :rtype:
        """
        return not is_empty_function(func=self.run)


# Class aliases
LinuxDaemon = UNIXDaemon
MacOSDaemon = UNIXDaemon
