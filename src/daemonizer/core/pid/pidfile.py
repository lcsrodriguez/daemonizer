"""Logic around PID file"""

import os
import random
import string
from multiprocessing.synchronize import Lock
from pathlib import Path

from daemonizer.constants import DEFAULT_PID_FILENAME_LENGTH
from daemonizer.exceptions import (
    InvalidPIDError,
    MissingPIDFileError,
)
from daemonizer.files import PID_FILES_DIR
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


def ensure_existing_path(path_: Path) -> None:
    """
    Function to ensure if a given path exists on the disk
    If not, create it and add it to the disk
    :param path_: Path to be checked
    :type path_: Path
    :return: None
    :rtype: Nothing
    """
    # logger.info(f"Checking path: {path_}")
    path_.mkdir(parents=True, exist_ok=True)


def generate_random_pid_name(length: int = DEFAULT_PID_FILENAME_LENGTH) -> str:
    """
    Function to generate a default PID file name with a random name
    :param length: PID name length
    :type length: int
    :return: Random PID file name
    :rtype: str
    """
    gen_pattern: str = string.ascii_letters + string.digits
    return "".join(random.choices(gen_pattern, k=length))


class Pidfile:
    """
    PID file handler
    """

    def __init__(
        self, pid_name: str | None = None, pidfile_path: Path | str | None = None
    ) -> None:
        """
        Constructor function to
        :param pid_name: PID name
        :type pid_name: str | None
        :param pidfile_path: PID file path (folder where to store the PID file)
        :type pidfile_path: Path | str | None
        """

        # Handling PID name
        if pid_name is None:
            # logger.warning("PID file name not specified. Generating a random one")
            self.pid_name: str = generate_random_pid_name()
        else:
            self.pid_name = pid_name

        # Handling PID file path (where to store PID file)
        if pidfile_path is None:
            # logger.info("PID file path not specified. Using default one")
            self.pidfile_path: Path = PID_FILES_DIR
            ensure_existing_path(path_=self.pidfile_path)

        else:
            # logging.info("Custom PID file path")
            if isinstance(pidfile_path, Path):
                self.pidfile_path = pidfile_path
                ensure_existing_path(path_=self.pidfile_path)
            elif isinstance(pidfile_path, str):
                self.pidfile_path = Path(pidfile_path)
                ensure_existing_path(path_=self.pidfile_path)

        # PID value
        self.pid_value: int = 0

        # PID filename
        self.pid_filename = f"{self.pid_name}.pid"

        # Get absolute math
        self.abs_path: str = self.get_abs_path()

        # Boolean to check if the pidfile exists in current filesystem
        self.is_active: bool = False

        self.lock: Lock | None = None

    def __str__(self) -> str:
        """
        Method to return a string representation of the class.
        :return: String representation of the class.
        :rtype: str
        """
        return f"Pidfile: {self.abs_path} [Active?: {self.is_active}]"

    def __repr__(self) -> str:
        """
        Method to return a string representation of the class.
        :return: String representation of the class.
        :rtype: str
        """
        return self.__str__()

    def is_existing_file(self) -> bool:
        """
        Method to check if the pidfile exists.
        :return: True if the pidfile exists, False otherwise.
        :rtype: bool
        """
        return os.path.isfile(self.abs_path)

    def get_abs_path(self) -> str:
        """
        Method to return the absolute path of the pidfile.
        (simple concatenation between pid_path and pid_filename)
        :return: The absolute path of the pidfile.
        :rtype: str
        """
        return os.path.join(self.pidfile_path, self.pid_filename)

    def write(self, pid: int | str = 0) -> bool:
        """
        Method to write the pid to the pidfile.
        :param pid: The pid to write to the pidfile.
        :type pid: int
        :return:
        :rtype: bool
        """

        if self.lock:
            self.lock.acquire(block=True)
            logger.info(f"BLOCKING LOCK A - {self.pid_filename}")

        pid = int(pid)
        self.pid_value = pid

        if self.is_existing_file():
            logger.info(f"toto: current -> {self.pid_filename}")
            # File is already existing
            i = 1
            self.pid_filename = f"{self.pid_name}_{i}.pid"
            self.abs_path = self.get_abs_path()

            # If file still exists, just pick the next one
            while os.path.isfile(self.abs_path):
                logger.info(f"tutu {i}")
                i += 1
                self.pid_filename = f"{self.pid_name}_{i}.pid"
                self.abs_path = self.get_abs_path()

        self.abs_path = self.get_abs_path()
        # raise AlreadyExistingPIDFileError("PID file already exists")
        logger.warning(self.abs_path)
        if pid <= 0:
            raise InvalidPIDError("Invalid pid value")

        try:
            with open(self.abs_path, "w") as pf:
                pf.write(str(pid) + "\n")
            self.is_active = True
            return True
        except IOError:
            return False
        finally:
            if self.lock:
                self.lock.release()
                logger.info(f"BLOCKING LOCK R - {self.pid_filename}")

    def read(self) -> int:
        """
        Method to read the pid from the pidfile.
        :return: The pid read from the pidfile.
        :rtype: int
        """

        if not self.is_existing_file():
            raise MissingPIDFileError("PID file does not exist")
        try:
            with open(self.abs_path, "r") as pf:
                return int(pf.read().strip())
        except (IOError, Exception):
            return 0

    def delete(self) -> bool:
        """
        Method to delete the pidfile.
        :return: True if the pidfile was deleted, False otherwise.
        :rtype: bool
        """
        if not self.is_existing_file():
            raise MissingPIDFileError("PID file does not exist")
        try:
            os.remove(self.abs_path)
            self.is_active = False
            return True
        except (IOError, Exception) as exc_:
            raise exc_
