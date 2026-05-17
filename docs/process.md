# Process


A process in UNIX/Linux is a **running instance of a program**.

## Identifiers

Here are the different identifiers for a given process:


| Identifier | Full Name          | Scope             | Purpose                            | Example                         |
|------------|--------------------|-------------------|------------------------------------|---------------------------------|
| **PID**    | Process ID         | Per process       | Unique identifier of a process     | `4123`                          |
| **PPID**   | Parent Process ID  | Per process       | PID of the process’s parent        | `4120`                          |
| **UID**    | User ID            | Per process       | User owner identity                | `1000`, `0` (`root`)            |
| **GID**    | Group ID           | Per process       | Primary group identity             | `1000`                          |
| **PGID**   | Process Group ID   | Per process group | Groups related processes together  | Shell pipelines                 |
| **SID**    | Session ID         | Per session       | Identifies a login/session leader  | Terminal session                |
| **TID**    | Thread ID          | Per thread        | Identifies a specific thread       | Linux thread identifier         |
| **TTY**    | Terminal ID        | Per process       | Controlling terminal               | `/dev/pts/0`                    |
