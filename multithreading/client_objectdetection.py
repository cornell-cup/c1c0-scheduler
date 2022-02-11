import client
import socket
import os 
import time
import sys

# Data communication process
if len(sys.argv)>1:
    argument = sys.argv[1]
    print(argument)
else:
    argument = "get data"
proc1 = client.Client("object-detection")
proc1.handshake()
arm_angle = '[10,20,30,40,50,60]' 
i = 0
while(i < 5):
    msg = 'arm ' + arm_angle
    proc1.communicate(msg)
    i = i + 1
    time.sleep(3)
proc1.close()
