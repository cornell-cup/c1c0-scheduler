from .. import client
import socket
import os 
import time
import sys

# Data communication process
if len(sys.argv) > 1:
    argument = sys.argv[1]
    print(argument)
else:
    argument = "get data"
proc1 = client.Client("path-planning")
proc1.handshake()

try:
    while True:
        proc1.communicate(argument)
        time.sleep(3)
finally:
    proc1.close()
