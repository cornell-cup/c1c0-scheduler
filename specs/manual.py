from scheduler.config import * # Configuration
from scheduler.utils import Message, DataQueue # Utilities

from typing import Optional # Type Hinting

def manual_check(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for manual_check messages.
    """

    # Returning identical message
    return msg

def manual_get(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for manual_get messages.
    """

    # Finding next task in queue
    item: Message = Message.decode(msg.data)
    fnd: Optional[Message] = queue.find(item.name, item.tag)

    # Returning task if found
    if fnd is not None: return fnd
    return Message(msg.name, msg.tag, DEFAULT_RESP)

def manual_put(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for manual_put messages.
    """

    # Adding task to queue
    item: Message = Message.decode(msg.data)
    queue.add(item)

    # Returning default response
    return Message(msg.name, msg.tag, DEFAULT_RESP)
