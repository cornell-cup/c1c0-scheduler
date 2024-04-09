from scheduler.config import * # Configuration
from scheduler.utils import Message, DataQueue # Utilities

from typing import Optional # Type Hinting

def movement_check(_: DataQueue, msg: Message) -> Message:
    """
    Handler for movement_check messages.
    """

    # Returning identical message
    return msg

def movement_get(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for movement_get messages.
    """

    # Finding next task in queue
    item: Optional[Message] = queue.find('xbox', 'put')
    if item is not None: return item
    return Message(msg.name, msg.tag, DEFAULT_RESP)
