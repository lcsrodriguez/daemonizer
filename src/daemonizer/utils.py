import os
import platform
from typing import Dict, Tuple

import distro

from .constants import UNIX_SYSTEM_NAMES


def check_os() -> Dict[str, str | os.uname_result | platform.uname_result]:
    """
    Function to check the operating system of the current machine.
    :return: A dictionary containing the operating system name and version.
    :rtype: dict
    """
    return {
        "os_name": os.name,
        "os_uname": os.uname(),
        "platform_details": platform.uname(),
    }


def get_unix_distro() -> str:
    """
    Function to get the Unix distribution name.
    :return: The Unix distribution name.
    :rtype: str
    """
    return distro.id()


class OSCheck:
    """
    Utils class **OSCheck**

    Class to check the operating system of the current machine.
    """

    __slots__: Tuple[str, ...] = ("",)

    @staticmethod
    def is_linux_machine() -> bool:
        """
        Method to check if the current machine is running a Linux operating system.
        :return: True if the machine is running Linux, False otherwise.
        :rtype: bool
        """
        return check_os()["platform_details"].system == "Linux"  # type: ignore[union-attr]

    @staticmethod
    def is_macos_machine() -> bool:
        """
        Method to check if the current machine is running a macOS operating system.
        :return: True if the machine is running macOS, False otherwise.
        :rtype: bool
        """
        return check_os()["platform_details"].system == "Darwin"  # type: ignore[union-attr]

    @staticmethod
    def is_windows_machine() -> bool:
        """
        Method to check if the current machine is running a Windows operating system.
        :return: True if the machine is running Windows, False otherwise.
        :rtype: bool
        """
        return check_os()["platform_details"].system == "Windows"  # type: ignore[union-attr]

    @staticmethod
    def is_unix_machine() -> bool:
        """
        Method to check if the current machine is running a Unix-like operating system.
        :return: True if the machine is running a Unix-like system, False otherwise.
        :rtype: bool
        """
        return check_os()["platform_details"].system in UNIX_SYSTEM_NAMES  # type: ignore[union-attr]

    @staticmethod
    def is_posix_compatible() -> bool:
        """
        Method to check if the current machine is POSIX compatible.
        :return: True if the machine is POSIX compatible, False otherwise.
        :rtype: bool
        """
        return check_os()["os_name"] == "posix"  # type: ignore[union-attr]
