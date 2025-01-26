from typing import Tuple
import os
from .exceptions import MissingPIDFileError, InvalidPIDError


class Pidfile:
    """
    Class **Pidfile**

    Simple class to handle pidfile operations.
    """

    __slots__: Tuple[str, ...] = ("pid_filename", "pid_path", "abs_path")

    def __init__(self, pid_filename: str = "", pid_path: str = "") -> None:
        """
        Constructor for **Pidfile** class.
        :param pid_filename:
        :type pid_filename: str
        :param pid_path: Path of the folder containing the pidfile
        :type pid_path: str
        """

        self.pid_filename: str = pid_filename
        self.pid_path: str = pid_path

        self.abs_path: str = self.get_abs_path()

    @property
    def absolute_path(self) -> str:
        """
        Property to return the absolute path of the pidfile.
        :return: The absolute path of the pidfile.
        :rtype: str
        """
        return self.abs_path

    @absolute_path.setter
    def absolute_path(self, value: str) -> None:
        """
        Setter for the absolute path of the pidfile.
        :param value: The new absolute path of the pidfile.
        :type value: str
        """
        self.abs_path = value

    def __str__(self) -> str:
        """
        Method to return a string representation of the class.
        :return: String representation of the class.
        :rtype: str
        """
        return f"Pidfile: {self.pid_path}/{self.pid_filename}"

    def __repr__(self) -> str:
        """
        Method to return a string representation of the class.
        :return: String representation of the class.
        :rtype: str
        """
        return self.__str__()

    def __eq__(self, other) -> bool:
        """
        Method to compare two objects.
        :param other: The other object to compare.
        :type other: object
        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Pidfile):
            return False
        return (
            self.pid_filename == other.pid_filename and self.pid_path == other.pid_path
        )

    def __hash__(self) -> int:
        """
        Method to return the hash of the object.
        :return: The hash of the object.
        :rtype: int
        """
        return hash((self.pid_filename, self.pid_path))

    def __bool__(self) -> bool:
        """
        Method to check if the current file exists
        :return: True if the object is valid, False otherwise.
        :rtype: bool
        """
        return self._existing_file()

    def _existing_file(self) -> bool:
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
        return os.path.join(self.pid_path, self.pid_filename)

    def write(self, pid: int | str = 0) -> bool:
        """
        Method to write the pid to the pidfile.
        :param pid: The pid to write to the pidfile.
        :type pid: int
        :return:
        :rtype: bool
        """
        pid = int(pid)

        if not self._existing_file():
            raise MissingPIDFileError("PID file does not exist")

        if pid <= 0:
            raise InvalidPIDError("Invalid pid value")

        try:
            with open(self.abs_path, "w") as pf:
                pf.write(str(pid))
            return True
        except IOError:
            return False
