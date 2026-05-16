"""CLI commands"""

from typing import Tuple

import click

from daemonizer.cli.processor import _cli_parse_daemons
from daemonizer.constants import APP_NAME, APP_VERSION
from daemonizer.core.daemons.flags import START
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
    _cli_parse_daemons(script, list(daemons), START, strict)
