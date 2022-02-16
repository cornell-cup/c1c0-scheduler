import threading
from abc import ABC, abstractmethod
from typing import Mapping, Callable, Iterable, Any, Tuple


class Worker(ABC, threading.Thread):
    """
    A worker object runs in the background and either listens to a resource
    or actuates on something.
    """
    stop_event = threading.Event()
    daemon = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def run(self) -> None:
        self.stop_event.clear()

    def stop(self) -> None:
        self.stop_event.set()


class DataProvider(ABC):
    """
    Often also Worker objects, DataProviders provide a continuous stream of
    data.
    """
    # Expected return value from Continuous response functions to the server
    new_data: threading.Condition = threading.Condition()
    data: Any
    is_data_provider = True


class System(ABC):
    """
    A system (usually for robotic system controls) that has various sensors
    and actuators. This ABC can be extended to provide the framework and any
    utilities to integrate various modules.
    """
    funcs = {}

    @abstractmethod
    def __init__(self, data_worker_info: Iterable[Tuple[str, int]],
                 controller_workers: int = 1, *args, d_data_workers: int = 0,
                 d_controller_workers: int = 0, **kwargs):
        """
        PARAMETERS
        ----------
        data_worker_info
            Iterable of port baudrate tuples. [(port, baudrate),...]. The
            number of entries determines the number of workers.
        controller_workers
            Number of controller workers to spawn.
        d_data_workers
            Number of data debugger workers to spawn.
        d_controller_workers
            Number of controller debugger workers to spawn
        """
        self.data_worker_info = data_worker_info
        self.controller_workers = controller_workers
        self.d_data_workers = d_data_workers
        self.d_controller_workers = d_controller_workers

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
