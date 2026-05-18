# CLI Reference

Here's the different commands available on the `daemonizer` CLI:

```shell


$ daemonizer version
$ daemonizer disclaimer


$ daemonizer start <path to script> DaemonClass1 DaemonName1 DaemonClass2 DaemonName2 ...
$ daemonizer stop <path to script> DaemonClass1 DaemonName1 DaemonClass2 DaemonName2 ...
$ daemonizer stop-name daemon_name
$ daemonizer stop-pid daemon_pid
$ daemonizer restart <path to script> DaemonClass1 DaemonName1 DaemonClass2 DaemonName2 ...
$ daemonizer status <path to script> DaemonClass1 DaemonName1 DaemonClass2 DaemonName2 ...
$ daemonizer ls
$ daemonizer pidfiles
$ daemonizer scan <path to script>
# It will scan all the daemon classes inside the input script and return their names
```

> [!NOTE]
> When running commands depending on a script, we always ask user to enter valid **daemon classes**.
> This is required to correctly identify valid daemons and execute the right primitive methods (start, stop, restart, status).
>
> These methods can indeed be overwritten by the user when defining its own daemon logic (in the script). In this case, the daemon class is needed as CLI input.

## `--help` dump

```shell
Usage: daemonizer [OPTIONS] COMMAND [ARGS]...

  CLI entry point

Options:
  --help  Show this message and exit.

Commands:
  ls         Listing all daemons currently found
  pidfiles   Get pid files folder.
  restart    Restart daemons (CLI target)
  scan       Scan daemons (CLI target)
  start      Start daemons (CLI target)
  status     Restart daemons (CLI target)
  stop       Stop daemons (CLI target)
  stop-name  Stop daemons via daemon's name input.
  stop-pid   Stop daemons via PID input.
  version    Version info
```


## Silence the disclaimer

By default, every CLI target has a disclaimer displayed on standard output (*stdout*) to make sure the user is aware of the risks while interacting with external daemons.

It is possible to turn it off manually:

```shell
$ daemonizer --no-disclaimer <command>
```

or via an environment variable:

```shell
export DAEMONIZER_DISCLAIMER=0
```

- set to 0 means no disclaimer displayed in this terminal session
- set to 1 means disclaimers will be displayed in this terminal session

> [!TIP]
> You can persist your choice by adding `export DAEMONIZER_DISCLAIMER=0` to your `~/.bashrc` file.

> [!TIP]
> You can erase your choice by: `unset DAEMONIZER_DISCLAIMER`
