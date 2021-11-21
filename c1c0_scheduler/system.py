import threading
from abc import ABC, abstractmethod
from typing import Mapping, Callable, Iterable


class Worker(ABC, threading.Thread):

    stop_event = threading.Event()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def run(self) -> None:
        self.stop_event.clear()

    def stop(self) -> None:
        self.stop_event.set()


class System(ABC):

    funcs = {}

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def start(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def stop(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get_workers(self) -> Iterable[Worker]:
        pass

    @abstractmethod
    def __enter__(self) -> 'System':
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def get_functionality(self) -> Mapping[str, Callable]:
        pass
