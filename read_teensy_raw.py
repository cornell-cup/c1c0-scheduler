import serial
import time
import sys

sys.path.append('../c1c0-movement/c1c0-movement/Locomotion')
import R2Protocol2 as r2p

ser = serial.Serial(
	port = '/dev/ttyTHS1',
	baudrate = 115200,
)
ser.close()
ser.open()
print(ser.name)

try:
    while True:
        s = ser.read(32)
        mtype, msg, status = r2p.decode(s)
        print(mtype, msg, status)
        #print(s)
        #time.sleep(3)
except KeyboardInterrupt:
    ser.close()