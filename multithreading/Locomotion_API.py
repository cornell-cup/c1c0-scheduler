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

def locomotion_msg(motor_power):
    try:
        msg = r2p.encode(bytes('loco','utf-8'), bytearray(motor_power.encode()))
        ser = serial_API.serial_init()
        ser.write(msg)
        ser.flush()
    except KeyboardInterrupt:
        ser.close()
def get_motor_msg(axis_x,axis_y):
    lvalue = 0
    rvalue = 0
    if(axis_x == 0 and axis_y == 1):
        lvalue = '+' + str(0.2) + '0'
        rvalue = '+' + str(0.2) + '0'
    elif(axis_x == 0 and axis_y == -1):
        lvalue = '-' + str(0.2) + '0'
        rvalue = '-' + str(0.2) + '0'
    elif(axis_x == -1 and axis_y == 0):
        lvalue = '-' + str(0.2) + '0'
        rvalue = '+' + str(0.2) + '0' 
    elif(axis_x == 1 and axis_y == 0):
        lvalue = '+' + str(0.2) + '0'
        rvalue = '-' + str(0.2) + '0'
    elif(axis_x == 0 and axis_y == 0):
        lvalue = '+' + str(0.) + '0'
        rvalue = '+' + str(0.) + '0'
    return 'xbox: (' + str(lvalue) + ',' + str(rvalue) + ')'
def zero():
    return 'xbox: (+0.00,+0.00)'