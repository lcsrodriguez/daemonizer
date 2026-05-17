# Daemon internals

> A **daemon** is a program that runs as a background process, rather than being under the direct control of an interactive user.



## How to daemonize a function

Here are all the methods to be defined:

- **`start`** := **`daemonize`** + **`run`**
- **`stop`** := kill process from (known/stored) PID
- **`restart`** : **`stop`** + **`start`**
- **`run`** := custom logic
- **`daemonize`** := apply *daemonization* procedure to get independent process

## Components

- PID file
  - `.pid` file extension
  - Stored in `/tmp/daemonizer/pidfiles/`
