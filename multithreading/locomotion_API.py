import serial
import time
import sys
import array
import struct

"""
Locomotion API for use with path_planning. 

"""
sys.path.append('/home/c1c0-main/c1c0-movement/c1c0-movement/Locomotion') #Might need to be resolved
import R2Protocol2 as r2p

ser = None


def init_serial(port, baud):
    """
    Opens serial port for locomotion communication
    port should be a string linux port: Ex dev/ttyTHS1
    Baud is int the data rate, commonly multiples of 9600
    """
    global ser
    ser = serial.Serial(port, baud)

def locomotion_msg(port, baud, motor_power):
    init_serial(port, baud)
    try:
        msg = r2p.encode(bytes('loco','utf-8'), bytearray(motor_power.encode()))
        #print(motor_power.encode())
        #print(len(motor_power.encode()))
        #print(len(msg))
        #print(msg)
        #print('\n')
        ser.write(msg)
        ser.flush()
    except KeyboardInterrupt:
        ser.close()
