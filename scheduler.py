from scheduler.config import * # Configuration
from scheduler.server import Server # Server
from scheduler.utils import Message, DataQueue # Utilities

from specs.facial import facial_check, facial_put, facial_get # Facial Specifications
from specs.manual import manual_check, manual_put, manual_get # Manual Specifications

from typing import Callable, Dict # Type Hinting

if __name__ == '__main__':
    # Initializing server and data queue
    scheduler: Server = Server()
    queue: DataQueue = DataQueue()

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        'facial_check': lambda msg: facial_check(queue, msg),
        'facial_get':   lambda msg: facial_get(queue, msg),
        'facial_put':   lambda msg: facial_put(queue, msg),

        'manual_check': lambda msg: manual_check(queue, msg),
        'manual_get':   lambda msg: manual_get(queue, msg),
        'manual_put':   lambda msg: manual_put(queue, msg),
    }

    # Attempting to start server
    attempt: int = 0
    while attempt < ATTEMPTS:
        if (scheduler.start()): break
        attempt += 1

    # Infinite loop for server
    while True:
        # Receiving message from client
        msg: Message = scheduler.receive()

        # Finding and calling handler for message
        search: str = f'{msg.name}{TAG_SEP}{msg.tag}'
        mapping.setdefault(search, lambda msg: msg)
        response: Message = mapping[search](msg)

        # Sending response to client
        scheduler.send(response)
