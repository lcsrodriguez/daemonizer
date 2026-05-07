"""Sample daemons to be used in scripts in examples/ folder"""

from datetime import datetime
from time import sleep

from daemonizer.core.daemons.logic import forever_loop
from daemonizer.core.daemons.unix import UNIXDaemon
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


class SampleDaemon1(UNIXDaemon):
    """
    Sample daemon 1
    """

    @forever_loop(catch_exceptions=False, after_delay=0.01)
    def run(self) -> None:
        """
        Function **run**
        Override of the `UNIXDaemon.run` function
        :return: Nothing
        :rtype: None
        """
        with open("/tmp/TOTO.log", "a") as f:
            f.write(f"Hello, Lucas {datetime.now()}\n")
            f.write(f"{self.get_arguments()['kwargs'].get('ssa', None)}\n")  # type: ignore[union-attr]
        sleep(1)


class SampleDaemon2(UNIXDaemon):
    """
    Sample daemon 2
    """

    @forever_loop(catch_exceptions=False, after_delay=0.01)
    def run(self) -> None:
        """
        Function **run**
        Override of the `UNIXDaemon.run` function
        :return: Nothing
        :rtype: None
        """
        with open("/tmp/TUTU.log", "a") as f:
            f.write(f"Hello, TUTU {datetime.now()}\n")
        sleep(1)
