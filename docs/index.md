# daemonizer


![PyPI - Version](https://img.shields.io/pypi/v/daemonizer-py) [![Linting](https://github.com/lcsrodriguez/daemonizer/actions/workflows/linting.yml/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/linting.yml) [![Docs](https://github.com/lcsrodriguez/daemonizer/actions/workflows/docs_build_deploy.yml/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/docs_build_deploy.yml) [![Publish](https://github.com/lcsrodriguez/daemonizer/actions/workflows/publish.yml/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/publish.yml) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Dependabot Updates](https://github.com/lcsrodriguez/daemonizer/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/lcsrodriguez/daemonizer/actions/workflows/dependabot/dependabot-updates) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/daemonizer-py) ![PyPI - Downloads](https://img.shields.io/pypi/dm/daemonizer-py)


Light-weight and easy-to-use Python package that simplifies the process of daemonizing Python applications,
allowing them to run in the background as standalone logics

It offers a programmatic way or CLI-first interface for developers, without using system-wise solutions like *services*.

## Features

- Simple API to daemonize any Python function or class
- Automatic handling of process management (PID files, logging, etc.)
- Support for start, stop, restart, and status operations
- Signal handling (SIGTERM, SIGINT, etc.)
- Compatible with UNIX-like systems
- Python 3.7+ support

## Getting started

1. Add `daemonizer` to your project

```shell
uv add daemonizer-py
```

or via `pip`: `pip install daemonizer-py`.

2. Define your daemon logic in a simple Python script `sample.py`:

```python linenums="1" hl_lines="10-15" title="Defining daemon logic"
from datetime import datetime
from time import sleep

from daemonizer.core.daemons.logic import forever_loop
from daemonizer.core.daemons.unix import UNIXDaemon
from daemonizer.utils.logs import get_logger

logger = get_logger(__name__)

class SampleDaemon(UNIXDaemon):
    @forever_loop(catch_exceptions=False, after_delay=0.01)
    def run(self) -> None:
        with open("/tmp/sample_daemon.log", "a") as f:
            f.write(f"Hello world, this is {datetime.now()}")
        sleep(1)
```

3. Interact with it either via the `daemonizer` **CLI**

```shell
$ daemonizer --no-disclaimer start sample.py SampleDaemon daemon_1
```

or directly via **SDK handler** (directly from Python scripts)

```python linenums="1" hl_lines="8-10" title="Daemon handler"

from daemonizer.core.handlers.ctx_manager import DaemonHandler
from .sample import SampleDaemon
from daemonizer.utils.logs import get_logger, setup_logger

setup_logger()
logger = get_logger(__name__)

with DaemonHandler() as h:
    d = SampleDaemon(name="daemon_1")
    h.start(d) # start daemon
```

> [!NOTE]
> Multiple daemons can be defined in a single file and multiple daemons can be managed under a single daemon handler (`DaemonHandler` instance).
