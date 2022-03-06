from typing import Optional

try:
    from .system import System
except ImportError:
    from c1c0_scheduler.system import System

system: Optional[System] = None
"""
The system most recently prepared. Only useful in use cases where only
one system is being utilized.
"""


DEBUG = True
"""
Changing the value of DEBUG during program execution does not have defined
behavior
"""


MAX_WORKERS = 10
"""
Number of workers for gRPC to use for the server process.
"""


def get_default() -> System:
    global system
    try:
        from .c1c0.system import C1C0System
        from .c1c0.config import DATA_WORKER_INFO
    except ImportError:
        from c1c0_scheduler.c1c0.system import C1C0System
        from c1c0_scheduler.c1c0.config import DATA_WORKER_INFO
    system = C1C0System(DATA_WORKER_INFO)
    return system
