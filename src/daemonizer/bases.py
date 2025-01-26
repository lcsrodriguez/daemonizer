from abc import ABC, abstractmethod


class Daemon(ABC):
    """
    Class **Daemon**

    Daemon base class to be inherited by other classes
    """

    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...

    @abstractmethod
    def restart(self): ...

    @abstractmethod
    def status(self): ...

    @abstractmethod
    def run(self): ...

    @abstractmethod
    def daemonize(self): ...

    @abstractmethod
    def _signal_handler(self, signum, frame): ...
