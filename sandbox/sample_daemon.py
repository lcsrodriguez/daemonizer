"""Sample daemon sandbox run"""

import datetime
import time

from daemonizer.core.daemons.unix import UNIXDaemon, handler
from daemonizer.core.pid.pidfile import Pidfile


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
