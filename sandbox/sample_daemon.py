"""Sample daemon sandbox run"""

import datetime
import time

from daemonizer.core.daemons.unix import UNIXDaemon
from daemonizer.core.handlers.base_handler import handler
from daemonizer.core.pid.pidfile import Pidfile
from daemonizer.utils.logs import get_logger, setup_logger

setup_logger()
logger = get_logger(__name__)


class SampleDaemon(UNIXDaemon):
    """
    Sandbox daemon
    """

    def run(self) -> None:
        """
        Function **run**
        :return: Nothing
        :rtype: None
        """
        while True:
            with open("/tmp/TOTO.log", "a") as f:
                f.write(f"Hello, Lucas {datetime.datetime.now()}\n")
            time.sleep(1)


if __name__ == "__main__":
    handler(
        SampleDaemon(
            name="TOTO", pidfile=Pidfile(pid_filename="TOTO.pid", pid_path="/tmp")
        )
    )
