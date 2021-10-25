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
while True:
    proc1.communicate(argument)
    time.sleep(3)
proc1.close()
