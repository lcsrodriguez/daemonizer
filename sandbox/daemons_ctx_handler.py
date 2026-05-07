"""Sandbox script to show DaemonHandler usage (context manager)"""

from daemonizer.core.handlers.ctx_manager import DaemonHandler
from daemonizer.samples.writers import SampleDaemon1, SampleDaemon2
from daemonizer.utils.logs import get_logger, setup_logger

setup_logger()
logger = get_logger(__name__)


# if __name__ == "__main__":
# Daemons handler
with DaemonHandler() as h:
    h.add(SampleDaemon1(name="daemon_1"))
    h.add(SampleDaemon2(name="daemon_2"))
