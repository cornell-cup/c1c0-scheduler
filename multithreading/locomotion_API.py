import serial
import time
import sys
import array
import struct
import serial_API

"""
Locomotion API for use with path_planning. 

"""
sys.path.append('/home/c1c0-main/c1c0-movement/c1c0-movement/Locomotion') #Might need to be resolved
import R2Protocol2 as r2p

def locomotion_msg(port, baud, motor_power):
    try:
        msg = r2p.encode(bytes('loco','utf-8'), bytearray(motor_power.encode()))
        #print(motor_power.encode())
        #print(len(motor_power.encode()))
        #print(len(msg))
        #print(msg)
        #print('\n')
        ser = serial_API.serial_init()
        ser.write(msg)
        ser.flush()
    except KeyboardInterrupt:
        ser.close()
