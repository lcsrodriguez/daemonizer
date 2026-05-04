"""UNIX daemon"""

import atexit
import logging
import os
import signal
import sys
import time
from enum import Enum
from typing import Tuple

from daemonizer.core.daemons.base import Daemon
from daemonizer.core.pid.pidfile import Pidfile
from daemonizer.exceptions import InvalidPIDFileError
from daemonizer.utils.func import gv, is_empty_function

Frame = type("Frame", (), {})


class StandardStreams(Enum):
    """Enum to store the standard streams"""

    IN = sys.stdin
    OUT = sys.stdout
    ERR = sys.stderr


class UNIXDaemon(Daemon):
    """
    Class **UNIXDaemon**

    Base class for creating UNIX daemons.
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

    def __init__(
        self,
        name: str = "",
        pidfile: str | Pidfile | None = None,
        working_directory: str = "/",
        umask: int = 0,  # 0o022
        logger: logging.Logger | None = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Constructor for **UNIXDaemon** class.
        :param name: Daemon name
        :type name: str
        :param pidfile: Path to the pidfile or an instance of the Pidfile class
        :type pidfile: str | Pidfile | None
        :param working_directory: Working directory for the daemon
        :type working_directory: str
        :param umask: Umask for the daemon
        :type umask: int
        :param args: Positional arguments
        :type args:
        :param kwargs: Keyword arguments
        :type kwargs:
        """
        if pidfile is None:
            raise InvalidPIDFileError("PID file is required")

        if isinstance(pidfile, str):
            _pidfile: Pidfile = Pidfile(
                pid_filename=pidfile, pid_path=kwargs.get("pid_path", "")
            )
        elif isinstance(pidfile, Pidfile):
            _pidfile = pidfile
        else:
            _pidfile = pidfile

        self.daemon_name: str = name if name != "" else "UNIX Daemon"
        self.pidfile: Pidfile = _pidfile
        self.daemon_pid: int = 0

        self.working_directory: str = working_directory
        self.umask: int = umask

        # Handling input logger
        self.logger: logging.Logger = (
            logger if logger is not None else logging.getLogger(__name__)
        )

        self.is_alive: bool = False

    def stop(self) -> None:
        """
        Function to stop the daemon
        :return: Nothing
        :rtype: None
        """
        if not self.pidfile.is_existing_file():
            gv(StandardStreams.ERR).write(
                f"Pidfile (file={self.pidfile.absolute_path}) does not exist. Daemon not running?\n"
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
                        f"Pidfile (file={self.pidfile.absolute_path}) deleted\n"
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
                f"Pidfile (file={self.pidfile.absolute_path}) already exists.Daemon already running?\n"
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
        :return: Nothing
        :rtype: None
        """
        self.stop()
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


def handler(daemon: UNIXDaemon) -> None:
    """
    Function to handle the daemon commands from user input.
    :param daemon: The daemon instance
    :type daemon: UNIXDaemon
    :return: Nothing
    :rtype: None
    """

    # sys.argv:  0 -> script name
    # sys.arg:  1 -> command
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            daemon.start()
        elif "stop" == sys.argv[1]:
            daemon.stop()
        elif "restart" == sys.argv[1]:
            daemon.restart()
        elif "status" == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print(f"usage: {sys.argv[0]} start|stop|restart")
        sys.exit(2)
