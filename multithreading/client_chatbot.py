import client
import socket
import os 
import time

# Simple communication test with a single process

proc1 = client.Client("Chatbot")
proc1.handshake()
#for i in range(0,10):
<<<<<<< Updated upstream
proc1.communicate("path-planning ('move-forward', 5.0)") #object-detection
=======
proc1.communicate("path-planning ('move forward', 3.0)")
# proc1.communicate("take attendance")
>>>>>>> Stashed changes
time.sleep(120)
proc1.close()
