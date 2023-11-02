import serial
import time
import sys
import array
import struct
sys.path.append('/home/ccrt/c1c0-movement/c1c0-movement/Locomotion') #Might need to be resolved
import R2Protocol2 as r2p
import serial_API

motor_angles = [0,0,0,0,0,0,0]
motor_index = 0

def arm_msg(port, baud, data):
    try:
        data_array = decode_scheduler(data)
        msg = r2p.encode(b"PRM", bytes(convert_16_to_8(data_array,len(motor_angles))))
        ser = serial_API.serial_init()
        ser.write(msg)
        ser.flush()
    except KeyboardInterrupt:
        ser.close()

def update_arm_msg(axis_x,axis_y):
    global motor_angles
    global motor_index
    if(axis_x == 0 and axis_y == 1):
        if(motor_index == 0):
            motor_angles[motor_index] += 3
        elif(motor_index == 2):
            motor_angles[motor_index] += 5
        else:
            motor_angles[motor_index] += 5
    elif(axis_x == 0 and axis_y == -1):
        if(motor_index == 0):
            motor_angles[motor_index] -= 3
        elif(motor_index == 2):
            motor_angles[motor_index] -= 5
        else:
            motor_angles[motor_index] -= 5
    elif(axis_x == -1 and axis_y == 0):
        motor_index -= 1
        if(motor_index == -1):
            motor_index = len(motor_angles)-1
    elif(axis_x == 1 and axis_y == 0):
        motor_index += 1
        if(motor_index == len(motor_angles)):
            motor_index = 0
    for index,angle in enumerate(motor_angles):
        if(angle < 0):
            motor_angles[index] = 0
            print(motor_angles[index])
    print(motor_angles)
    print("motor J" + str(motor_index+1))

def get_arm_msg():
    global motor_angles
    return 'precise: '+ str(motor_angles)
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
