import serial
import time
import sys
import array
import struct
sys.path.append('/home/ccrt/c1c0-movement/c1c0-movement/Locomotion') #Might need to be resolved
import R2Protocol2 as r2p

ser = None
def init_serial(port,baud):
	'''
	Initializes the serial port, usually set baud to 9600
	'''
	global ser
	ser =serial.Serial(port,baud)

def arm_msg(port, baud, arm_angle):
	init_serial(port, baud)
	try: 
		msg = r2p.encode(bytes('PRM','utf-8'), bytearray(arm_angle.encode()))
		print(msg)
		ser.write(msg)
	except KeyboardInterrupt:
		ser.close()
