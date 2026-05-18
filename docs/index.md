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

2. Define your daemon logic in a simple Python script
3. Interact with it either via **SDK handler** (directly from Python scripts) or via the `daemonizer` **CLI**
