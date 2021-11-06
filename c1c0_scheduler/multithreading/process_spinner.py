from .config import ProcessTypes, PType, extract_process_type

import sys
import subprocess
import socket
from typing import Tuple


def spin(process_type_: PType) -> Tuple[subprocess.Popen, socket.socket]:
    process_type = extract_process_type(process_type_)
    argument = None
    pid = subprocess.Popen([sys.executable, "client_pathplanning.py", argument])
    soc = socket.socket()
    return pid, soc
