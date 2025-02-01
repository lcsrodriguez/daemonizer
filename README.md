# daemonizer

Light-weight and easy-to-use Python package that simplifies the process of daemonizing Python applications,
allowing them to run in the background as standalone logics.

## Features

- Simple API to daemonize any Python function or class
- Automatic handling of process management (PID files, logging, etc.)
- Support for start, stop, restart, and status operations
- Signal handling (SIGTERM, SIGINT, etc.)
- Compatible with UNIX-like systems
- Python 3.7+ support

## Installation

Install using pip:

```bash
pip install daemonizer
```

## Usage

Create a Python script `main.py` with the following content:
```python
import datetime, time

from daemonizer.unix_daemon import UNIXDaemon, handler
from daemonizer.pidfile import Pidfile

class TestDaemon(UNIXDaemon):
    def run(self):
        while True:
            with open("/tmp/test_daemon.log", "a") as f:
                f.write(f"Hello, current time is: {datetime.datetime.now()}\n")
            time.sleep(1)

if __name__ == "__main__":
    handler(TestDaemon(name="test_daemon", pidfile=Pidfile(pid_filename="test_daemon.pid", pid_path="/tmp")))
```


The package provides a simple command-line interface to interact with the daemonized process.
The following commands are available:

```bash
$ python3 main.py {start,stop,restart,status}
```

## Contribute

```
git clone https://github.com/lcsrodriguez/daemonizer.git
cd daemonizer/
pip install -r requirements.txt
pip install -r requirements-dev.txt

pre-commit
pre-commit install
```
