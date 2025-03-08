import numpy as np # Standard Python Imports
import signal, time

from api.locomotionAPI import zero_locomotion # Locomotion Utilities
from api.preciseAPI import zero_precise # Precise Utilities
from api.rotateAPI import zero_rotate # Rotate Utilities
from api.strongAPI import zero_strong # Strong Utilities

from scheduler.camera import Camera # Camera
from scheduler.config import * # Configuration
from scheduler.server import Server # Server
from scheduler.utils import Message, DataQueue # Utilities

from specs.chatbot import chatbot_check, chatbot_put, chatbot_get # Chatbot Specifications
from specs.facial import facial_check, facial_put, facial_get # Facial Specifications
from specs.manual import manual_check, manual_put, manual_get # Manual Specifications
from specs.movement import movement_check, movement_get # Movement Specifications
from specs.controller import controller_check, controller_put # Controller Specifications

from typing import Callable, Dict, Union # Type Hinting


def clean_exit(sig, frame) -> None:
    """
    Function to perform a clean exit, when the program is interrupted.
    """
    global scheduler, queue, camera
    queue.add(Message('xbox', 'put', zero_locomotion()))
    queue.add(Message('xbox', 'put', zero_strong()))
    queue.add(Message('xbox', 'put', zero_precise()))
    queue.add(Message('xbox', 'put', zero_rotate()))
    print("Performing Clean Exit Of Scheduler...")


if __name__ == '__main__':
    # Initializing server and data queue
    scheduler: Server = Server()
    queue: DataQueue = DataQueue()
    camera: Camera = Camera()

    # Setting up signal handler
    signal.signal(signal.SIGTERM, clean_exit)
    kill_now: bool = False
    kill_num: int = 20

    # Opening Camera
    with camera as cam:

        # Initializing response handlers and mapping
        mapping: Dict[str, Callable[[str], None]] = {
            'chatbot_check': lambda msg: chatbot_check(queue, msg),
            'chatbot_get':   lambda msg: chatbot_get(queue, msg),
            'chatbot_put':   lambda msg: chatbot_put(queue, msg),

            'facial_check': lambda msg: facial_check(queue, msg),
            'facial_get':   lambda msg: facial_get(queue, msg),
            'facial_put':   lambda msg: facial_put(queue, msg),

            'manual_check': lambda msg: manual_check(queue, msg),
            'manual_get':   lambda msg: manual_get(queue, msg),
            'manual_put':   lambda msg: manual_put(queue, msg),

            'movement_check': lambda msg: movement_check(queue, msg),
            'movement_get':   lambda msg: movement_get(queue, msg),

            'xbox_check': lambda msg: controller_check(queue, msg),
            'xbox_put':   lambda msg: controller_put(queue, msg),

            'camera_get': lambda _: cam.adjust_read() if CAMERA_MODE else None,
        }

        # Attempting to start server
        attempt: int = 0
        while attempt < ATTEMPTS:
            if (scheduler.start()): break
            attempt += 1

        # Infinite loop for server
        while kill_num > 0:
            # Receiving message from client
            msg: Message = scheduler.receive()
            if (kill_now): kill_num -= 1

            # Finding and calling handler for message
            search: str = f'{msg.name}{TAG_SEP}{msg.tag}'
            mapping.setdefault(search, lambda msg: msg)
            response: Union[Message, np.ndarray] = mapping[search](msg)

            # Sending response to client
            if isinstance(response, Message): scheduler.send(response)
            else: scheduler.send_image(response)
