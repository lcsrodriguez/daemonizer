import os
import sys
from enum import Enum
from typing import List, Tuple

from .bases import Daemon
from .exceptions import InvalidPIDFileError
from .pidfile import Pidfile
from .utils import gv

__all__: List[str] = ["UNIXDaemon", "LinuxDaemon", "MacOSDaemon"]


class StandardStreams(Enum):
    """Enum to store the standard streams"""

    IN = sys.stdin
    OUT = sys.stdout
    ERR = sys.stderr


class UNIXDaemon(Daemon):
    __slots__: Tuple[str, ...] = (
        "pidfile",
        "daemon_name",
        "daemon_pid",
    )

    def __init__(
        self, name: str = "", pidfile: str | Pidfile | None = None, *args, **kwargs
    ) -> None:
        """
        Constructor for **UNIXDaemon** class.
        :param name: Daemon name
        :type name: str
        :param pidfile: Path to the pidfile or an instance of the Pidfile class
        :type pidfile: str | Pidfile | None
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

    def stop(self):
        pass

    def start(self):
        pass

    def restart(self):
        pass

    def status(self):
        pass

    def run(self):
        pass

    def daemonize(self) -> None:
        """
        Daemonize the process by applying the UNIX double fork method.
        :return: Nothing
        :rtype: None
        """

        # Perform first fork

        try:
            _pid = os.fork()
            if _pid > 0:  # Exit first parent
                sys.exit(0)
        except OSError as exc_:
            sys.stderr.write(f"Fork 1 has failed: {exc_.errno}({exc_.strerror})\n")
            sys.exit(1)

        # Decouple first child from parent process environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

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

    def _signal_handler(self, signum, frame):
        pass


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
