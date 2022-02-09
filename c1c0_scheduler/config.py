from types import ModuleType
from typing import Optional

from .system import System

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

def init_c1c0() -> System:
    global system
    from .c1c0.system import C1C0System
    system = C1C0System()
    system.start()
    return system


def init_default() -> System:
    return init_c1c0()
