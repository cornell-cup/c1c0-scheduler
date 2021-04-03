import client
import socket
import os 
import time

proc1 = client.Client("path-planning")
proc1.handshake()
for i in range(0,10):
    proc1.communicate("move to Mars")
    time.sleep(3)
proc1.close()
