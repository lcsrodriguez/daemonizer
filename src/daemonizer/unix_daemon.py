from .bases import Daemon


class UNIXDaemon(Daemon): ...


# Class aliases
LinuxDaemon = UNIXDaemon
MacOSDaemon = UNIXDaemon
