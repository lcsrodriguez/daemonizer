from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List

from .exceptions import InvalidUNIXDistroError


@dataclass
class UNIXOSConfig:
    """Dataclass to store the configuration of the OS"""

    distro_id: str
    name: str
    pidfile_path: List[str]


class UNIXOSConfigEnum(Enum):
    """
    Enum to store the list of configuration for most major OS

    Supported OS list: https://distro.readthedocs.io/en/latest/#distro.id
    Below pidfile path are used by default in case the user does not provide any path when creating the daemon
    """

    DEBIAN = UNIXOSConfig(
        distro_id="debian", name="Debian", pidfile_path=["/run", "/var/run"]
    )

    UBUNTU = UNIXOSConfig(
        distro_id="ubuntu", name="Ubuntu", pidfile_path=["/run", "/var/run"]
    )

    ARCH = UNIXOSConfig(distro_id="arch", name="Arch", pidfile_path=["/run"])

    MACOS = UNIXOSConfig(
        distro_id="darwin",
        name="macOS",
        pidfile_path=["/var/run", "/private/var/run", "/Library"],
    )

    @classmethod
    def get_mapping(cls) -> Dict[str, Any]:
        return {os.value.distro_id: os for os in cls}

    @classmethod
    def get_enum(cls, distro_id: str) -> UNIXOSConfig:
        try:
            return cls.get_mapping()[distro_id]
        except KeyError:
            raise InvalidUNIXDistroError(f"OS {distro_id} is not supported")

    @classmethod
    def get_pidfile_paths(cls, distro_id) -> List[str]:
        try:
            return cls.get_mapping()[distro_id].value.pidfile_path
        except KeyError:
            raise InvalidUNIXDistroError(f"OS {distro_id} is not supported")
