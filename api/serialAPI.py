import serial # Standard Python Imports

from scheduler.config import * # Configurations
from scheduler.utils import printc # Utilities

PORT: str      = '/dev/ttyTHS1'
BAUDRATE: int  = 115200
TIMEOUT: float = .1

ser: any = None

def serial_init():
    """
    Initialize the serial connection with the specified port and baudrate.

    @return: The serial connection object.
    """

    global ser
    if ser: return ser
    ser = serial.Serial(PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
    return ser

def serial_write(data):
    """
    Write the given data to the serial connection.

    @param data: The data to write to the serial connection.
    """

    global ser
    if ser: ser.write(data)
    printc(f'[{data}]', INF_COLOR)
    ser.flush()

def serial_close():
    """
    Close the serial connection.
    """

    global ser
    if ser: ser.close()
