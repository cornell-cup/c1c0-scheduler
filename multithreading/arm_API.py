import serial
import time
import sys
import array
import struct
sys.path.append('/home/ccrt/c1c0-movement/c1c0-movement/Locomotion') #Might need to be resolved
import R2Protocol2 as r2p
import serial_API

ser = None


def arm_msg(port, baud, data):
    try:
        data_array = decode_scheduler(data)
        print(data_array)
        msg = r2p.encode(b"PRM", bytes(convert_16_to_8(data_array,6)))
        print(msg)
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
    arr = data.split('[')[1].split(']')[0].split(',')
    return [int(i.strip()) for i in arr]
    

def convert_16_to_8(msg, length):
    data = []
    for i in range(0,length):
        data.append((msg[i] >> 8) & 255)
        data.append(msg[i] & 255)
    return data
