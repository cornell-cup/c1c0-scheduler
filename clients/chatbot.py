import sys, time # Default Python Libraries
path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path

from scheduler.config import * # Configuration
from scheduler.client import Client as SClient # Scheduler Client
from scheduler.utils import Message, printc # Utilities

from client.audio import speech_to_text, recognize_C1C0, remove_C1C0  # Audio Interface
from client.client import OpenAPI # Client Interface

from labels.config import recognize as config_recognize, handler as config_handler  # Configuration Specifications
from labels.general import recognize as general_recognize, handler as general_handler  # General Info Specifications
from labels.movement import recognize as movement_recognize, handler as movement_handler  # Movement Specifications
from labels.facial import recognize as facial_recognize, handler as facial_handler  # Facial Specifications

from typing import Callable, Dict # Type Hinting

if __name__ == '__main__':
    # Initializing clients
    chatbot_client: OpenAPI = OpenAPI()
    scheduler_client: SClient = SClient('chatbot')
    scheduler_client.connect()

    # Initialzing response handlers and mapping
    mapping: Dict[str, Callable[[str], None]] = {
        config_recognize:   lambda msg: config_handler(chatbot_client, msg, scheduler_client),
        general_recognize:  lambda msg: general_handler(chatbot_client, msg, scheduler_client),
        movement_recognize: lambda msg: movement_handler(chatbot_client, msg, scheduler_client),
        facial_recognize:   lambda msg: facial_handler(chatbot_client, msg, scheduler_client)
    }

    # Infinite loop for chatbot
    while True:
        # Receiving audio from user and checking for C1C0 name
        msg: str = speech_to_text()
        print(f"\033[32mUser: {msg}\033[0m")
        if msg is None or not recognize_C1C0(msg):
            print('C1C0 Command Not Recognized.')
            continue

        # Removing C1C0 name from message
        msg = remove_C1C0(msg)
        print(f"\033[32mCommand: {msg}\033[0m")

        # Finding and calling handler for message
        for (recognize, handler) in mapping.items():
            if recognize(chatbot_client, msg):
                handler(msg); break
