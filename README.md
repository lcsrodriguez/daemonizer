# daemonizer

[![Linting](https://github.com/lcsrodriguez/daemonizer/actions/workflows/linting.yml/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/linting.yml)
[![Docs](https://github.com/lcsrodriguez/daemonizer/actions/workflows/docs_build_deploy.yml/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/docs_build_deploy.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Dependabot Updates](https://github.com/lcsrodriguez/daemonizer/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/dependabot/dependabot-updates)

Light-weight and easy-to-use Python package that simplifies the process of daemonizing Python applications,
allowing them to run in the background as standalone logics.

## Features

- Simple API to daemonize any Python function or class
- Automatic handling of process management (PID files, logging, etc.)
- Support for start, stop, restart, and status operations
- Signal handling (SIGTERM, SIGINT, etc.)
- Compatible with UNIX-like systems
- Python 3.7+ support

## Getting started

Install package using `uv` or `pip`:

```shell
uv add daemonizer-py # pip install daemonizer-py
```

Create a Python script `daemon.py` where you can define your daemon logic following below framework:

```python
from datetime import datetime
from time import sleep

from daemonizer.core.daemons.logic import forever_loop
from daemonizer.core.daemons.unix import UNIXDaemon

class SampleDaemon(UNIXDaemon):
    """ Sample daemon """

    @forever_loop(catch_exceptions=False, after_delay=0.01)
    def run(self) -> None:
        with open("/tmp/hello_daemon.log", "a") as f:
            f.write(f"Hello, World {datetime.now()}\n")
            f.write(f"{self.kwargs().get('ssa', None)}\n")
        sleep(1)
```

Defining a daemon is very simple:
1. Create a subclass of `UNIXDaemon`
2. Just overload the `run(...)` method with your logic to be executed in the daemon

> [!NOTE]
> No need to worry about `while True:` loop. If you decorate the `run(...)` method with the `@forever_loop(...)` decorator,
> the logic defined inside will be **executed infinitely**.
>
> Optional arguments are available for the `@forever_loop(...)` decorator. (See docs)

Once defined, you can start a daemon using two methods:

- Using `handler` func:
```python
if __name__ == "__main__":
    handler(SampleDaemon(name="daemon_1"))
```

```shell
uv run daemon.py [start|stop|restart|status]
```

- Using context manager handler with ` DaemonHandler()`:
```python
from daemonizer.core.handlers.ctx_manager import DaemonHandler
# Daemons handler
with DaemonHandler() as h:
    h.start(SampleDaemon1(name="daemon_1"))
    h.start(SampleDaemon2(name="daemon_2"))
```

> [!WARNING]
> Daemon should have a **unique** name at global level (no duplicate).

- Using CLI:

```shell
daemonizer start daemon.py # START op will be performed on all daemons defined in this file
daemonizer start daemon.py SampleDaemon1 # START op will be performed **ONLY** on `SampleDaemon1` defined in this file
```

- Using API or web-app *(WIP)*

The package provides a simple command-line interface to interact with the daemonized process.
The following commands are available:

```bash
$ python3 main.py {start,stop,restart,status}
```

## Contribute

Clone the repo, improve the code base and submit a pull request

```shell
git clone https://github.com/lcsrodriguez/daemonizer.git
cd daemonizer/
uv sync
pre-commit install-hooks
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
