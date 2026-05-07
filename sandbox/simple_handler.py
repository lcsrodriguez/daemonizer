"""Sample daemon sandbox run"""

from daemonizer.core.handlers.base_handler import handler
from daemonizer.samples.writers import SampleDaemon1
from daemonizer.utils.logs import get_logger, setup_logger

setup_logger()
logger = get_logger(__name__)


if __name__ == "__main__":
    handler(SampleDaemon1(name="e"))
