import os
from typing import Dict
import platform


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


class OSCheck:
    @staticmethod
    def is_linux_machine() -> bool:
        """
        Method to check if the current machine is running a Linux operating system.
        :return: True if the machine is running Linux, False otherwise.
        :rtype: bool
        """
        return platform.system() == "Linux"

    @staticmethod
    def is_macos_machine() -> bool:
        """
        Method to check if the current machine is running a macOS operating system.
        :return: True if the machine is running macOS, False otherwise.
        :rtype: bool
        """
        return platform.system() == "Darwin"

    @staticmethod
    def is_windows_machine() -> bool:
        """
        Method to check if the current machine is running a Windows operating system.
        :return: True if the machine is running Windows, False otherwise.
        :rtype: bool
        """
        return platform.system() == "Windows"
