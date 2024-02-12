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
        ack_decoded = ""
        # loop if acknowledgement not correct
        while ack_decoded != "ack":
            ser.write(msg)
            ack = ser.read_until(expected = b'\xd2\xe2\xf2') #Tail bits of r2p encoded message, see r2protocol.encode() specification
            ack_decoded = r2p.decode(ack)
            print(ack_decoded)
        # finish and say I just sent it
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