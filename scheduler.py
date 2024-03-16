from scheduler.config import * # Configuration
from scheduler.server import Server # Server
from scheduler.util import Message, DataQueue # Utilities

from typing import Callable, Dict, Optional, Tuple # Type Hinting

def manual_put(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for manual_put messages.
    """

    # Adding task to queue
    item: Message = Message.decode(msg.data)
    queue.add(item)
    return Message(msg.name, msg.tag, DEFAULT_RESP)

def manual_get(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for manual_get messages.
    """

    # Finding next task in queue
    item: Message = Message.decode(msg.data)
    fnd: Optional[Message] = queue.find(item.name, item.tag)
    if fnd is not None: return fnd
    return Message(msg.name, msg.tag, DEFAULT_RESP)

def facial_get(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for facial_get messages.
    """

    # Finding next task in queue
    item: Optional[Message] = queue.find(msg.name, msg.tag)
    if item is not None: return item
    return Message(msg.name, msg.tag, DEFAULT_RESP)

def facial_put(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for facial_put messages.
    """

    # Adding data to queue
    queue.add(msg)
    return Message(msg.name, msg.tag, DEFAULT_RESP)

if __name__ == '__main__':
    # Initializing server and data queue
    scheduler: Server = Server()
    queue: DataQueue = DataQueue()

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        'manual_check': lambda msg: msg,
        'manual_put':   lambda msg: manual_put(queue, msg),
        'manual_get':   lambda msg: manual_get(queue, msg),

        'facial_check': lambda msg: msg,
        'facial_put':   lambda msg: facial_put(queue, msg),
        'facial_get':   lambda msg: facial_get(queue, msg),
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
