"""Sandbox script to show DaemonHandler usage (context manager)"""

from daemonizer.core.handlers.ctx_manager import DaemonHandler
from daemonizer.samples.writers import SampleDaemon1  # , SampleDaemon2
from daemonizer.utils.logs import get_logger, setup_logger

setup_logger()
logger = get_logger(__name__)


# if __name__ == "__main__":
# Daemons handler
with DaemonHandler() as h:
    # h.start(SampleDaemon1(name="daemon_1"))

    d1 = SampleDaemon1(name="daemon_1")
    h.start(d1)
    # sleep(3)
    # h.status(d1)

    # h.start(SampleDaemon1(name="daemon_1"))
    # h.start(SampleDaemon2(name="daemon_2"))
    # h.start(SampleDaemon1(name="daemon_1"))
    # h.start(SampleDaemon2(name="daemon_2"))
    # h.start(SampleDaemon1(name="daemon_1"))
    # h.start(SampleDaemon1(name="daemon_1"))
    # h.start(SampleDaemon2(name="daemon_2"))

    # h.start
    # h.stop
    # h.status
    # h.restart
