import serial
import time
import sys
import array
import struct

"""
Locomotion API for use with path_planning. 

"""
sys.path.append('/home/ccrt/c1c0-movement/c1c0-movement/Locomotion') #Might need to be resolved
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
		ser.write(msg)		
		time.sleep(0.1)
	except KeyboardInterrupt:
		ser.close()
	
						
#if __name__ == '__main__':
	#init_serial('/dev/ttyTHS1', 9600)
	#if len(sys.argv) != 2:
	#	print("need 1 argument: tuple command for locomotion")
	#motor_power = sys.argv[1]
	#array1 = [10,60,30,40,50,60]
	#s = struct.Struct('13s')
	#motor_power_array = s.pack(motor_power.encode('utf-8'))
	#motor_power_array = bytearray(motor _power.encode('utf-8'))
	#print(motor_power_array)
	#s = struct.Struct('4s')
	#type_data = "loco"
	#type_data_array = s.pack(type_data.encode('utf-8'))
	#type_data_array = bytearray(type_data.encode('utf-8'))
	#encoded = r2p.encode(type_data_array, motor_power_array)
	#print(encoded)
	#print(type_data_array)
	#try:
		#while True:
	#		start = time.time()
	#		print("start time: " + str(start))
	#		msg = r2p.encode(bytes('loco','utf-8'), bytearray(motor_power.encode()))
	#		print(msg)
	#		ser.write(msg)	
	#		print(r2p.decode(msg))		
	#		time.sleep(0.1)
	#		end = time.time()
	#		print("end time: " + str(end))	
	#		elapse = end - start
	#		print("elapsed time: " + str(elapse))
	#except KeyboardInterrupt:
		ser.close()
