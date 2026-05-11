"""CLI commands"""

import click

from daemonizer.constants import APP_NAME, APP_VERSION
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
