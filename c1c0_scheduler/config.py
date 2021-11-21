from types import ModuleType
from typing import Optional

from .system import System

system: Optional[System] = None


def init_c1c0() -> System:
    global system
    from .c1c0.system import C1C0System
    system = C1C0System()
    system.start()
    return system

