"""Handler logic for UNIX daemons"""

import sys

from daemonizer.core.daemons.unix import UNIXDaemon
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


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
            logger.info("[START]")
            daemon.start()

        elif "stop" == sys.argv[1]:
            logger.info("[STOP]")
            daemon.stop()

        elif "restart" == sys.argv[1]:
            logger.info("[RESTART]")
            daemon.restart()

        elif "status" == sys.argv[1]:
            logger.info("[STATUS]")
            daemon.status()

        else:
            logger.error("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        logger.error(f"usage: {sys.argv[0]} start|stop|restart")
        sys.exit(2)
