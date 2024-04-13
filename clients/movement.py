import sys, time # Default Python Libraries
path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path

from typing import List # Typing

from scheduler.config import * # Configuration
from scheduler.client import Client # Client
from scheduler.utils import Message, printc # Utilities

from api.serialAPI import serial_init, serial_write, serial_close # Serial Connection
from api.locomotionAPI import locomotion_decode # Locomotion Decoding
from api.preciseAPI import precise_decode # Precise Decoding
from api.strongAPI import strong_decode # Strong Decoding
from api.rotateAPI import rotate_decode # Rotate Decoding

import R2Protocol2 as r2p # Serial encoding/decoding protocol

STALL: int = .01 # Time To Wait For New Task

def convert_16_to_8(arr: str, length: int) -> List[int]:
    """
    Convert the given array from 16-bit to 8-bit format.

    @param arr: The array to convert.
    @param length: The length of the message.
    @return: The converted message.
    """

    data = []
    for i in range(0,length):
        data.append((arr[i] >> 8) & 255)
        data.append(arr[i] & 255)
    return data

def locomotion_serial(data: str) -> None:
    """
    Send the given data (encoded in locomotion format) to the specified serial port.

    @param data: The data (encoded in locomotion format) to send.
    """

    try:
        movement: str = locomotion_decode(data)
        mtype: str    = bytes('loco','utf-8')
        encode: str   = bytearray(movement.encode())
        message: str  = r2p.encode(mtype, encode)

        serial_init()
        serial_write(message)
    except KeyboardInterrupt:
        serial_close()

def precise_serial(data: str) -> None:
    """
    Send the given data (encoded in precise format) to the specified serial port.

    @param data: The data (encoded in precise format) to send.
    """

    try:
        angles: list[int] = precise_decode(data)
        mtype: str        = b"PRM"
        encode: str       = bytes(convert_16_to_8(angles, len(angles)))
        message: str      = r2p.encode(mtype, encode)

        serial_init()
        serial_write(message)
    except KeyboardInterrupt:
        serial_close()

def strong_serial(data: str) -> None:
    """
    Send the given data (encoded in strong format) to the specified serial port.

    @param data: The data (encoded in strong format) to send.
    """

    try:
        array: list[int] = strong_decode(data)
        mtype: str          = b"STR"
        encode: str         = bytes(convert_16_to_8(array, len(array)))
        message: str        = r2p.encode(mtype, encode)

        serial_init()
        serial_write(message)
    except KeyboardInterrupt:
        serial_close()

def rotate_serial(data: str) -> None:
    """
    Send the given data (encoded in rotate format) to the specified serial port.

    @param data: The data (encoded in rotate format) to send.
    """

    try:
        rotate = rotate_decode(data)
        mtype: str =  bytes("head", "utf-8")
        encode: str = bytearray(rotate.encode())
        message: str = r2p.encode(mtype, encode)

        serial_init()
        serial_write(message)
    except KeyboardInterrupt:
        serial_close()

if __name__ == '__main__':
    # Initializing client
    client: Client = Client('movement')
    client.connect()

    while True:
        # Asking ZMQ for next task
        time.sleep(STALL)
        response: Message = client.communicate('get', 'null')

        # Getting the task
        data: str = response.data
        if (data == DEFAULT_RESP): continue
        if (data == 'exit' or data == 'quit'): break

        # Sending task to serial
        if ('locomotion' in data): locomotion_serial(data)
        elif ('precise' in data):  precise_serial(data)
        elif ('strong' in data):   strong_serial(data)
        elif ('rotate' in data):   rotate_serial(data)
        else: printc(f'Invalid command: {data}', ERR_COLOR)

    # Closing client
    client.close()
    printc('Program terminated.', INF_COLOR)
