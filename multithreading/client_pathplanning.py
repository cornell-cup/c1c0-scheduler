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
argument_list = ["(+0.01,+0.01)", "(+1.25,+0.25)", "(-0.15,+0.15)", "(+0.15,-0.15)", "(-0.05,-0.05)"]
argument = ["(+0.15,+0.15)", "(+0.15,-0.15)", "(-0.15,+0.15)", "(+0.00,+0.00)", "(-0.15,+0.15)", "(+0.15,-0.15)", "(+0.00,+0.00)"]
for motor_power in argument:
    msg = "locomotion " + motor_power#"(+0.00,+0.00)"
    print(msg)
    resp = proc1.communicate(msg)
    time.sleep(2)
proc1.close()
