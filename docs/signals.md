# Signals

In UNIX/Linux, a **signal** is a lightweight asynchronous notification sent to a process (or thread) by:

- the kernel,
- another process,
- or the process itself.

Signals are used to notify a program that some event occurred.

> [!WARNING]
> A signal can arrive at almost any moment while the program runs; that’s why signal handlers must be implemented very carefully and not be used as standard IPC data streams.

## List

> [!WARNING]
> Signal numbers can vary slightly across Unix variants (Linux, BSD, macOS, Solaris). The numbers below are the typical Linux/x86_64 values.

| Number | Name                | Default Action | Typical Usage                               | Catchable? |
|--------|---------------------|----------------|---------------------------------------------|------------|
| 1      | `SIGHUP`            | Terminate      | Terminal closed, reload config for daemons  | Yes        |
| 2      | `SIGINT`            | Terminate      | Interrupt from keyboard (`Ctrl+C`)          | Yes        |
| 3      | `SIGQUIT`           | Core dump      | Quit from keyboard (`Ctrl+\`)               | Yes        |
| 4      | `SIGILL`            | Core dump      | Illegal CPU instruction                     | Yes        |
| 5      | `SIGTRAP`           | Core dump      | Breakpoint/debug trap                       | Yes        |
| 6      | `SIGABRT`           | Core dump      | Abort signal from `abort()`                 | Yes        |
| 7      | `SIGBUS`            | Core dump      | Bus error / invalid memory access           | Yes        |
| 8      | `SIGFPE`            | Core dump      | Arithmetic exception (divide by zero, etc.) | Yes        |
| 9      | `SIGKILL`           | Terminate      | Forcefully kill process                     | **No**     |
| 10     | `SIGUSR1`           | Terminate      | User-defined signal 1                       | Yes        |
| 11     | `SIGSEGV`           | Core dump      | Segmentation fault                          | Yes        |
| 12     | `SIGUSR2`           | Terminate      | User-defined signal 2                       | Yes        |
| 13     | `SIGPIPE`           | Terminate      | Write to broken pipe/socket                 | Yes        |
| 14     | `SIGALRM`           | Terminate      | Timer alarm from `alarm()`                  | Yes        |
| 15     | `SIGTERM`           | Terminate      | Graceful termination request                | Yes        |
| 16     | `SIGSTKFLT`         | Terminate      | Stack fault (obsolete/Linux-specific)       | Yes        |
| 17     | `SIGCHLD`           | Ignore         | Child process stopped/exited                | Yes        |
| 18     | `SIGCONT`           | Continue       | Resume stopped process                      | Yes        |
| 19     | `SIGSTOP`           | Stop           | Pause process immediately                   | **No**     |
| 20     | `SIGTSTP`           | Stop           | Terminal stop (`Ctrl+Z`)                    | Yes        |
| 21     | `SIGTTIN`           | Stop           | Background process reading terminal         | Yes        |
| 22     | `SIGTTOU`           | Stop           | Background process writing terminal         | Yes        |
| 23     | `SIGURG`            | Ignore         | Urgent socket condition                     | Yes        |
| 24     | `SIGXCPU`           | Core dump      | CPU time limit exceeded                     | Yes        |
| 25     | `SIGXFSZ`           | Core dump      | File size limit exceeded                    | Yes        |
| 26     | `SIGVTALRM`         | Terminate      | Virtual timer expired                       | Yes        |
| 27     | `SIGPROF`           | Terminate      | Profiling timer expired                     | Yes        |
| 28     | `SIGWINCH`          | Ignore         | Terminal window resized                     | Yes        |
| 29     | `SIGIO` / `SIGPOLL` | Terminate      | Async I/O available                         | Yes        |
| 30     | `SIGPWR`            | Terminate      | Power failure warning                       | Yes        |
| 31     | `SIGSYS`            | Core dump      | Bad system call                             | Yes        |

## Non-catchable signals

Only these two standard signals cannot be caught, blocked, or ignored by any user-space program:

| Signal           | Purpose                            |
|------------------|------------------------------------|
| `SIGKILL` (`9`)  | Immediately terminate a process    |
| `SIGSTOP` (`19`) | Immediately stop/suspend a process |


These are enforced by the kernel to guarantee administrative control over processes.

> [!TIP]
> To list all signals available on your system, run below command:
>
> ```shell
> kill -l
> ```

## Signals commonly used signals in practice

| Signal    | Typical command              |
|-----------|------------------------------|
| `SIGTERM` | `kill PID`                   |
| `SIGKILL` | `kill -9 PID`                |
| `SIGINT`  | `Ctrl+C`                     |
| `SIGTSTP` | `Ctrl+Z`                     |
| `SIGCONT` | `kill -CONT PID`             |
| `SIGHUP`  | Reload daemon config         |
| `SIGCHLD` | Parent notified child exited |
