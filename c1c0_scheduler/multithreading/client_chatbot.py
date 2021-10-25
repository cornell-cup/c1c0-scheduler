import client
import socket
import os 
import time

# Simple communication test with a single process

proc1 = client.Client("Chatbot")
proc1.handshake()
for i in range(0,10):
    proc1.communicate("Weather")
    time.sleep(3)
proc1.close()
