"""CLI commands"""

from typing import Tuple

import click

from daemonizer.cli.daemon_loader import find_daemon_classes, load_module_from_script
from daemonizer.cli.processor import _cli_parse_daemons
from daemonizer.constants import APP_NAME, APP_VERSION
from daemonizer.core.daemons.flags import RESTART, START, STATUS, STOP
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
    Start daemons (CLI target)
    :return: Nothing
    :rtype: None
    """
    _cli_parse_daemons(script, list(daemons), START, strict)


# Command: $ daemonizer stop
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
def stop(script: str, daemons: Tuple[str, ...], strict: bool) -> None:
    """
    Stop daemons (CLI target)
    :return: Nothing
    :rtype: None
    """
    _cli_parse_daemons(script, list(daemons), STOP, strict)


# Command: $ daemonizer restart
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
def restart(script: str, daemons: Tuple[str, ...], strict: bool) -> None:
    """
    Restart daemons (CLI target)
    :return: Nothing
    :rtype: None
    """
    _cli_parse_daemons(script, list(daemons), RESTART, strict)


# Command: $ daemonizer status
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
def status(script: str, daemons: Tuple[str, ...], strict: bool) -> None:
    """
    Restart daemons (CLI target)
    :return: Nothing
    :rtype: None
    """
    _cli_parse_daemons(script, list(daemons), STATUS, strict)


# Command: $ daemonizer scan
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
@click.option(
    "--strict/--no-strict",
    "-s",
    type=click.BOOL,
    is_flag=True,
    required=False,
    default=True,
)
def scan(script: str, strict: bool) -> None:
    """
    Scan daemons (CLI target)
    :return: Nothing
    :rtype: None
    """
    click.echo(f"Scan | Script: {script} - Strict: {strict}")

    module = load_module_from_script(script_path=script)

    daemon_classes = find_daemon_classes(module=module, strict=strict)
    click.echo(f"Found {len(daemon_classes)} daemon classes")
    for i, daemon_class in enumerate(daemon_classes):
        click.echo(
            f"{i + 1} \t {daemon_class.__name__} - (module: {daemon_class.__module__})"
        )
