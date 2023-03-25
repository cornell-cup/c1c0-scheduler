import random
import serial
import time 
import R2Protocol2 as r2p
#import modified_protocol2 as r2p

ser = None

#Opens the serial port to the Arduino, must be called at the beginning before using any other functions
def open():
	global ser
	ser = serial.Serial(
	    port = '/dev/ttyTHS1',
	    baudrate = 9600,
	)

#Closes the serial port to the Arduino, must be called at the end of the program
def close():
	global ser
	ser.close()

#Call this method to return the head to 90 degrees
def zero():
	return headRotate(0, 0, 1)
	time.sleep(0.2)

#Call this method when the left bumper is held to get the head to rotate to the left at a predetermined rate
def leftButton():
	return headRotate(5, 1, 0)
	time.sleep(0.2)

#Call this method when the right bumper is held to get the head to rotate to the right at a predetermined rate
def rightButton():
	return headRotate(5, 0, 0)
	time.sleep(0.2)

#Call this method to turn to a specific angle between 0 and 202 degrees (boundaries are for these testing purposes with the HS-755HB servo, but are different from the one on C1C0)
def turnToAngle(angle):
	headRotate(angle, 0, 1)

#This method takes information about the angle of rotation and sends it to the arduino to turn the servo
#    ang : int, 0 <= ang <= 202, angle to turn (either to or for) 
#    negative : bool, 1 if the angle is negative from the current position (only necessary when the angle is a change in)
#    absolute : bool, 1 if the ang given is an absolute angle, 0 if ang is a change in angle
def headRotate(ang, negative, absolute):
	address = 3
#	ang = 20
#	absolute = 0
#	negative = 0
	#data = bytearray((ang).to_bytes(1,'big') + (absolute).to_bytes(1,'big') + (negative).to_bytes(1,'big')) + bytearray([0,0,0,0,0]) + str.encode("head", "utf-8")
	data = 'head rot: ' + str(ang) + str(absolute) + str(negative)
	#msg = r2p.encode(bytes("head","utf-8"),(address).to_bytes(1,'big'),data) 
	#print(msg)
	#print(len(msg))
	#ser.write(msg)
	return data

def init_serial(port, baud):
    """
    Opens serial port for locomotion communication
    port should be a string linux port: Ex dev/ttyTHS1
    Baud is int the data rate, commonly multiples of 9600
    """
    global ser
    ser = serial.Serial(port, baud)

def head_msg(port, baud, data):
    init_serial(port, baud)
    try:
        msg = r2p.encode(bytes("head","utf-8"), bytearray(data.encode()))
        #print(data.encode())
        #print(len(motor_power.encode()))
        #print(len(msg))
        #print(msg)
        #print('\n')
        ser.write(msg)
        time.sleep(0.1)
    except KeyboardInterrupt:
        ser.close()

