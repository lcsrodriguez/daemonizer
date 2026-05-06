"""Sandbox script to show DaemonHandler usage (context manager)"""

from daemonizer.core.handlers.ctx_manager import DaemonHandler
from daemonizer.utils.logs import get_logger
from sandbox.sample_daemon import SampleDaemon

logger = get_logger(__name__)

# Daemons handler
with DaemonHandler() as h:
    h.add(SampleDaemon(name="Toto"))
    h.add(SampleDaemon())
