import client
import socket
import os 
import time
import serial
import sys

# Accessing serial data without depending on the scheduler

sys.path.append('../../c1c0-movement/c1c0-movement/Locomotion')
import R2Protocol2 as r2p
Data = {}

ser = serial.Serial(
	port = '/dev/ttyTHS1',
	baudrate = 115200,
)
ser.close()
ser.open()
print(ser.name)

proc1 = client.Client("path-planning")
proc1.handshake()
for i in range(0,40):
    s = ser.read(32) #reads serial buffer for terabee
    Data['terabee1'] = "" #clears previous values
    mtype, msg, status = r2p.decode(s) #decodes serial message (see R2Protocol2.py)
    if(status == 1):
        # print(type(mtype))
        for i in range(len(msg)): #loop through length of data
            if i % 2 == 0:
                # Data['terabee1'] += str(ord(msg[i])) + str(ord(msg[i+1])) + "," #assemble char values into int16s and put them in Data dictionary as a string
                Data['terabee1'] += str(msg[i]*256 + msg[i+1]) + "," #assemble char values into int16s and put them in Data dictionary as a string
    elif(status == 0):
        print("Incorrect Checksum")
    print(Data['terabee1'])
proc1.close()

