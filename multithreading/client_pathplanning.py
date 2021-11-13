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
proc1 = client.Client("path-planning")
proc1.handshake()
i = 0
while(i < 5):
    resp = proc1.communicate(argument)
    i = i + 1
    time.sleep(3)
proc1.close()
