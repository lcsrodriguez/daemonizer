"""Core logic to:
(1) scan external Python scripts requested by CLI users when interacting with daemons,
(2) collect all classes inheriting from Daemon or UNIXDaemon base classes
(3) Instantiate one object per class found to start these daemons when CLI users request it
"""

import importlib.util
import inspect
from _frozen_importlib import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any, List, Type

from daemonizer.core.daemons.base import Daemon
from daemonizer.core.daemons.unix import UNIXDaemon
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


def load_module_from_script(script_path: Path | str | None = None) -> ModuleType | None:
    """
    Function to load a specific module from a given input Python script
    :param script_path: Input script path
    :type script_path: Path | str | None
    :return: Module object imported via importlib.util if successful, None otherwise
    :rtype: ModuleType | None
    """

    if script_path is None:
        return None

    if isinstance(script_path, str):
        script_path = Path(script_path)

    # Making the path absolute, resolving all symlinks
    path: Path = script_path.resolve()

    # Checking extension (.py)
    extension: str = "".join(path.suffixes)
    if extension not in [".py", ".pyi"]:
        logger.error(f"Script extension {extension} not supported")
        return None

    # Module name (final path component, without its suffix)
    module_name = path.stem

    logger.info(f"Loading module {module_name} from script {path.absolute()}")

    # A factory function for creating a ModuleSpec instance based on the path to a file
    # ModuleSpec := A specification for a module’s import-system-related state
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        logger.error("Module spec import failed (importlib)")
        return None

    # Create a new module based on spec
    module: ModuleType | None = importlib.util.module_from_spec(spec)

    if module is None:
        logger.error("Module creation from spec failed (importlib)")
        return None

    # spec.loader (:= an object that loads a module)
    if spec.loader is None:
        logger.error("Module creation from spec failed (importlib)")
        return None

    # Loading module in current context
    # (executes the module in its own namespace when a module is imported or reloaded)
    spec.loader.exec_module(module=module)
    return module


def find_daemon_classes(
    module: ModuleType | None = None, strict: bool = True
) -> List[Type]:
    """
    Function to scan input module and collect + return a list of specific daemon classes
    :param module: Input module
    :type module: ModuleType | None
    :param strict: Return only (True) the classes from the script itself (not those imported to the script from other sub-modules/dependencies)
    :type strict: bool
    :return: List of daemon classes
    :rtype: List[Type]
    """

    daemons: List[Type] = []
    if module is None or not isinstance(module, ModuleType):
        logger.error("Input module is invalid")
        return daemons

    for e, cls in inspect.getmembers(module, inspect.isclass):
        # Skipping UNIXDaemon itself (not relevant)
        if cls is UNIXDaemon or cls is Daemon:
            continue

        if issubclass(cls, UNIXDaemon):  # mro check otherwise
            if strict:
                # Handling case where we only want daemons from the script itself (not from its dependencies)
                if cls.__module__ != module.__name__:
                    continue
            daemons.append(cls)

    return daemons


def get_daemon_instances(daemons: List[Type] | None = None) -> List[Any]:
    """
    Function to get daemon instances from daemon classes
    :param daemons: Input daemon classes
    :type daemons: List[Type] | None
    :return: List of daemon objects (1 y input daemon class)
    :rtype: List[Any]
    """

    daemon_instances: List[Any] = []
    if daemons is None:
        return daemon_instances

    for daemon in daemons:
        daemon_instances.append(daemon())

    return daemon_instances
