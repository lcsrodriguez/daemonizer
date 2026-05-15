"""CLI commands"""

from pathlib import Path
from typing import Callable, List, Tuple

import click

from daemonizer.cli.daemon_loader import (
    find_daemon_classes,
    get_daemon_instances,
    load_module_from_script,
)
from daemonizer.constants import APP_NAME, APP_VERSION
from daemonizer.core.daemons.flags import (
    DEFAULT_FLAG,
    FLAGS,
    RESTART,
    START,
    STATUS,
    STOP,
)
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)


# Entry point
@click.group()
def cli() -> None:
    """
    CLI entry point
    :return: Nothing
    :rtype: None
    """
    pass


# Command: $ daemonizer version
@cli.command()
def version() -> None:
    """
    Version info
    :return: Nothing
    :rtype: None
    """
    click.echo(f"{APP_NAME} v{APP_VERSION}")


# Command: $ daemonizer start
@cli.command()
@click.argument(
    "script",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    required=True,
)
@click.argument("daemons", type=click.STRING, required=False, nargs=-1)
@click.option(
    "--strict/--no-strict",
    "-s",
    type=click.BOOL,
    is_flag=True,
    required=False,
    default=True,
)
def start(script: str, daemons: Tuple[str, ...], strict: bool) -> None:
    """
    Start a daemon (CLI target)
    :return: Nothing
    :rtype: None
    """
    # click.echo(f"START")
    click.echo(f"script: {script}")
    click.echo(f"daemons: {daemons}")

    click.echo(f"strict: {strict}")

    """
    daemon_instances = get_daemon_instances(
        daemons=find_daemon_classes(
            module=load_module_from_script(script_path=script),
            strict=True),
        only_includes=list(daemons)
    )
    """
    _cli_parse_daemons(script, list(daemons), START, strict)

    # click.echo(f"Daemon instances: {daemon_instances}")

    # Reach input script on machine and import modules (logic inside)
    # Scan for daemons (if 1 daemon is specified, only focus on this one, otherwise instantiate all daemons)
    # Instantiate a new daemon object


def _cli_parse_daemons(
    script: str | Path | None = None,
    exclusive_daemon_classes: List[str] | None = None,
    flag_operation: int = DEFAULT_FLAG,
    strict: bool = True,
) -> None:
    """
    This function will parse the CLI request including:
    - input script path
    - specific daemons to run or everything found
    - operation to apply on these daemons
    :param script: Input script path
    :type script: str | Path | None
    :param exclusive_daemon_classes: List of specific daemon classes to be run (against the logic scanned from the module). If nothing is specified, all daemons from the module must be considered.
    :type exclusive_daemon_classes: List[str] | None
    :param flag_operation: Flag of the operation to perform on considered daemons
    :type flag_operation: int
    :param strict: True if only daemons from current modules should be considered, False otherwise (all daemons including from dependencies)
    :type strict: bool
    :return: Nothing
    :rtype: None
    """

    if script is None:
        return None

    if isinstance(script, str):
        script = Path(script)

    if isinstance(exclusive_daemon_classes, tuple):
        exclusive_daemon_classes = list(exclusive_daemon_classes)

    assert isinstance(exclusive_daemon_classes, list), "Daemons must be a list"

    # Loading module
    module = load_module_from_script(script_path=script)

    # Finding daemon classes in module
    daemon_classes = find_daemon_classes(module=module, strict=strict)
    click.echo(f"Classes: {daemon_classes}")

    # Getting daemon instances
    daemon_instances = get_daemon_instances(
        daemons=daemon_classes, only_includes=exclusive_daemon_classes
    )
    click.echo(f"Instances: {daemon_instances}")

    # Getting correct operation from input flag
    func: Callable = _get_op_func_from_flag(flag_operation=flag_operation)

    # For each daemon instances, execute the given function
    for daemon_instance in daemon_instances:
        # getattr(daemon_instance, func)()
        # daemon_instance.func()
        func(
            daemon_instance
        )  # clean form as we have a lambda func whose unique parameter is the daemon instance itself
    return None


def _get_op_func_from_flag(flag_operation: int) -> Callable:
    """
    This function will return a function that will run the specified operation,
    translated from the input flag operation. This is somehow a *mapping* function
    :param flag_operation: Valid input flag operation
    :type flag_operation: int
    :return: Lambda function that will run the specified operation once called with a valid `Daemon` instance
    :rtype: Callable
    """
    if flag_operation not in FLAGS:
        return lambda _: None

    if flag_operation == START:
        return lambda x: x.start()
    elif flag_operation == STOP:
        return lambda x: x.stop()
    elif flag_operation == STATUS:
        return lambda x: x.status()
    elif flag_operation == RESTART:
        return lambda x: x.restart()
    else:
        return lambda x: None
