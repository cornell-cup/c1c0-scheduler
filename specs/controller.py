from scheduler.config import * # Configuration
from scheduler.utils import Message, DataQueue # Utilities

from typing import Optional # Type Hinting

def controller_check(_: DataQueue, msg: Message) -> Message:
    """
    Handler for controller_check messages.
    """

    # Returning identical message
    return msg

def controller_put(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for conroller_put messages.
    """

    # Adding data to queue
    queue.add(msg)
    return Message(msg.name, msg.tag, DEFAULT_RESP)
