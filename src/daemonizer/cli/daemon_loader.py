"""Core logic to:
(1) scan external Python scripts requested by CLI users when interacting with daemons,
(2) collect all classes inheriting from Daemon or UNIXDaemon base classes
(3) Instantiate one object per class found to start these daemons when CLI users request it
"""

import importlib.util
from _frozen_importlib import ModuleSpec
from pathlib import Path
from types import ModuleType

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

    # Module name (final path component, without its suffix)
    module_name = path.stem

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
