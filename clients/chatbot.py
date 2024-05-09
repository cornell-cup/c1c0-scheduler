import sys, time # Default Python Libraries
path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path

from scheduler.config import * # Configuration
from scheduler.client import Client as SClient # Scheduler Client
from scheduler.utils import Message, printc # Utilities

from client.client import OpenAPI # Client Interface

from labels.error import handler as error_handler # Error Specifications
from labels.general import desc as general_desc, handler as general_handler # General Specifications
from labels.movement import desc as movement_desc, handler as movement_handler # Movement Specifications
from labels.recognition import desc as recognition_desc, handler as recognition_handler # Recognition Specifications

from typing import Callable, Dict # Type Hinting

if __name__ == '__main__':
    # Initializing clients
    chatbot_client: OpenAPI = OpenAPI()
    scheduler_client: SClient = SClient('chatbot')
    scheduler_client.connect()

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        general_desc:     lambda msg: general_handler(chatbot_client, msg),
        movement_desc:    lambda msg: movement_handler(chatbot_client, msg),
        recognition_desc: lambda msg: recognition_handler(chatbot_client, msg)
    }

    # Infinite loop for chatbot
    while True:
        # Receiving message from user
        msg: str = input('You: ')
        if msg == 'exit' or msg == 'quit': break

        # Finding and calling handler for message
        label: str = chatbot_client.categorize(msg, list(mapping.keys()))
        mapping.setdefault(label, lambda msg: error_handler(chatbot_client, msg))
        data1, data2 = mapping[label](msg)

        # Sending message to scheduler
        response1: Message = scheduler_client.communicate('put', data1)
        time.sleep(7)

        # Receiving response from scheduler
        response2: Message = scheduler_client.communicate('get', data2)
        print(response2.data.strip('][\'').split(', ')[0])

    # Closing client
    scheduler_client.close()
    printc('Program terminated.', INF_COLOR)
