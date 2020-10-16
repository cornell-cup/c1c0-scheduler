
import serial
import time

ser_strong = serial.Serial('/dev/strongarm', 9600)

'''
time.sleep(1)
while(True):
    ser_strong.write("M2DN999E".encode('utf-8'))
    time.sleep(2)
    ser_strong.write("M2DN800E".encode('utf-8'))
    time.sleep(2)
    #ser_strong.write("M2DN595E".encode('utf-8'))
    #time.sleep(1)
    #ser_strong.write("M1DN625E".encode('utf-8'))
    #time.sleep(1)
    #ser_strong.write("M2DP595E".encode('utf-8'))
    #time.sleep(1)
    
    #if ser_strong.inWaiting():
    #print(ser_strong.readline())
# ser_strong.close()
'''
def lift():
    for i in range(0,100):
        ser_strong.write("M2DN1900E".encode('utf-8'))
        time.sleep(1)
        #ser_strong.write("M2DN800E".encode('utf-8'))
        time.sleep(1)
    ser_strong.close()
lift()
