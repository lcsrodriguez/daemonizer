from typing import Tuple

from .bases import Daemon
from .exceptions import InvalidPIDFileError
from .pidfile import Pidfile


class UNIXDaemon(Daemon):
    __slots__: Tuple[str, ...] = (
        "pidfile",
        "daemon_name",
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

    def daemonize(self):
        pass

    def _signal_handler(self, signum, frame):
        pass


# Class aliases
LinuxDaemon = UNIXDaemon
MacOSDaemon = UNIXDaemon
