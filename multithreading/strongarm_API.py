import serial
import random
import time 
import R2Protocol2 as r2p
import serial_API
"""
Strong Arm API to use with multserver
"""

data = [3, 3, 3, 3] # data[elbow, spin, hand, shoulder]
# Elbow:    3-stop,  1-in,    2-out
# Spin:     3-stop,  1-CW,    2-CCW
# Hand:     3-stop,  1-close, 2-open
# Shoulder: 3-stop,  1-up,    2-down

def strong_scheduler(data):
    return 'strong: ' + str(data)

def move_elbow(dir=0):
    if dir == 1: data[0] = 1
    elif dir == 2: data[0] = 2
    else: data[0] = 3
    return strong_scheduler(data)

def move_spin(dir=0):
    if dir == 1: data[1] = 1
    elif dir == 2: data[1] = 2
    else: data[1] = 3
    return strong_scheduler(data)
    
def move_hand(dir=0):
    if dir == 1: data[2] = 1
    elif dir == 2: data[2] = 2
    else: data[2] = 3
    return strong_scheduler(data)
    
def move_shoulder(dir=0):
    if dir == 1: data[3] = 1
    elif dir == 2: data[3] = 2
    else: data[3] = 3
    return strong_scheduler(data)

def zero():
    global data
    data = [3,3,3, 3]
    return strong_scheduler(data)

def strong_msg(data):
    try:
        data_array = decode_scheduler(data)
        msg = r2p.encode(b"STR", bytes(convert_16_to_8(data_array,4)))
        ser = serial_API.serial_init()
        ser.write(msg)
        ser.flush()
    except KeyboardInterrupt:
        ser.close()

def decode_scheduler(data):
    """
    Decodes scheduler string data in format 'strong: [1,2,3,3]' back into an array of four numbers as [1,2,3,3]
    """
    data = str(data)
    a = int(data[9])
    b = int(data[12])
    c = int(data[15])
    d = int(data[18])
    return [a, b, c, d]

def convert_16_to_8(msg, length):
    data = []
    for i in range(0,length):
        data.append((msg[i] >> 8) & 255)
        data.append(msg[i] & 255)
    return data
