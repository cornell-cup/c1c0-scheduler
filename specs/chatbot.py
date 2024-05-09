from scheduler.config import * # Configuration
from scheduler.utils import Message, DataQueue # Utilities

from typing import Optional # Type Hinting

def chatbot_check(_: DataQueue, msg: Message) -> Message:
    """
    Handler for chatbot_check messages.
    """

    # Returning identical message
    return msg

def chatbot_get(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for chatbot_get messages.
    """

    # Finding next task in queue
    item: Message = Message.decode(msg.data)
    fnd: Optional[Message] = queue.find(item.name, item.tag)

    # Returning task if found
    if fnd is not None: return fnd
    return Message(msg.name, msg.tag, DEFAULT_RESP)

def chatbot_put(queue: DataQueue, msg: Message) -> Message:
    """
    Handler for chatbot_put messages.
    """

    # Adding task to queue
    item: Message = Message.decode(msg.data)
    queue.add(item)

    # Returning default response
    return Message(msg.name, msg.tag, DEFAULT_RESP)
