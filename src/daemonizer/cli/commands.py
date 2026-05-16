"""CLI commands"""

import glob
import signal
from pathlib import Path
from typing import List, Tuple

import click

from daemonizer.cli.daemon_loader import find_daemon_classes, load_module_from_script
from daemonizer.cli.processor import _cli_parse_daemons, _stop_pid
from daemonizer.constants import APP_NAME, APP_VERSION
from daemonizer.core.daemons.flags import RESTART, START, STATUS, STOP
from daemonizer.files import PID_FILES_DIR
from daemonizer.utils.logs import get_logger
from daemonizer.utils.process import is_active_process

logger = get_logger(__name__)


# Entry point
@click.group()
def cli() -> None:
    """
    CLI entry point
    """
    pass


# Command: $ daemonizer version
@cli.command()
def version() -> None:
    """
    Version info
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
    """
    click.echo(f"Scan | Script: {script} - Strict: {strict}")

    module = load_module_from_script(script_path=script)

    daemon_classes = find_daemon_classes(module=module, strict=strict)
    click.echo(f"Found {len(daemon_classes)} daemon classes")
    for i, daemon_class in enumerate(daemon_classes):
        click.echo(
            f"{i + 1} \t {daemon_class.__name__} - (module: {daemon_class.__module__})"
        )


# Command: $ daemonizer stop-pid
@cli.command()
@click.argument("pids", type=click.INT, required=False, nargs=-1)
@click.option(
    "--signal",
    "-g",
    type=click.INT,
    is_flag=False,
    required=False,
    default=signal.SIGTERM,
)
def stop_pid(pids: Tuple[int, ...], signal: int) -> None:
    """
    Stop daemons via PID input.
    This command is recommended if you already have the daemon's PID.
    On signal reception, daemon will kill stop itself, clean the on-disk PID file and stop the process.
    :param pids: PIDs
    :type pids: Tuple[int, ...]
    :param signal: Signal to be used
    :type signal: int
    """
    click.echo("Stop pids: " + str(pids))

    for pid in pids:
        if pid <= 0:
            click.echo("PID must be strictly greater than 0")
            return None

    # TODO: check on signal input

    for pid in pids:
        _stop_pid(pid=pid, sig=signal)
    return None


# Command: $ daemonizer stop-name
@cli.command()
@click.argument("names", type=click.STRING, required=False, nargs=-1)
@click.option(
    "--signal",
    "-g",
    type=click.INT,
    is_flag=False,
    required=False,
    default=signal.SIGTERM,
)
def stop_name(names: Tuple[str, ...], signal: int) -> None:
    """
    Stop daemons via daemon's name input.
    This command is recommended if you already have the daemon names.
    """
    click.echo("Stop daemon names: " + str(names))

    for daemon_name in names:
        pid: int = -1

        # Cleaning daemon name
        if daemon_name.endswith(".pid"):
            daemon_name = daemon_name.replace(".pid", "")

        # Getting daemon name
        p = PID_FILES_DIR / Path(daemon_name + ".pid")

        if p.exists():
            with open(p.absolute(), "r") as f:
                pid = int(f.readline().strip())
                _stop_pid(pid=pid, sig=signal)
        else:
            click.echo(f"PID file for this daemon's name: {daemon_name} does not exist")


# Command: $ daemonizer ls
@cli.command()
def ls() -> None:
    """
    Listing all daemons currently found
    """
    pattern = PID_FILES_DIR / "*.pid"
    found_daemons: List[str] = sorted(glob.glob(pattern.__str__()))

    for i, daemon in enumerate(found_daemons):
        pidfile: Path = Path(daemon).absolute()

        daemon_name: str = pidfile.stem

        with open(pidfile.absolute(), "r") as f:
            pid = int(f.readline().strip())

        is_active_daemon: bool = is_active_process(pid_=pid)
        click.echo(
            f"({i + 1}) {daemon_name} | PID := {pid} | Active?: {is_active_daemon}"
        )


# Command: $ daemonizer pidfiles
@cli.command()
def pidfiles() -> None:
    """
    Get pid files folder. This can be used to `cd $(daemonizer pidfiles)`
    """
    click.echo(PID_FILES_DIR.__str__())
