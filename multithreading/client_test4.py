import client
import socket
import os 
import time

# Data communication process

proc1 = client.Client("object-detection")
proc1.handshake()
while(True):
    proc1.communicate("get data")
    time.sleep(3)
proc1.close()