from scheduler.config import * # Configuration
from scheduler.utils import Message, DataQueue # Utilities

from typing import Optional # Type Hinting

def facial_check(_: DataQueue, msg: Message) -> Message:
    """
    Handler for facial_check messages.
    """

    # Returning identical message
    return msg

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
