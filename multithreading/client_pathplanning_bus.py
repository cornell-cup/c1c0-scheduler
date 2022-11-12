import client
import socket
import os 
import time
import sys

sys.path.append("/home/c1c0-main/c1c0-ece/")
sys.path.append('/home/c1c0-main/c1c0-movement/c1c0-movement/Locomotion')

import TEST_API
import R2Protocol2 as r2p



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

ser = TEST_API.init_serial('/dev/ttyTHS1', 115200)
counter = 0
ser.reset_input_buffer()
ser.reset_output_buffer()

while(True):
    
    for motor_power in argument:
        msg = "locomotion " + motor_power#"(+0.00,+0.00)"
        print(msg)
        resp = proc1.communicate(msg)
        #time.sleep(0.5)
    
    # ~ msg = r2p.encode(b"LOC", bytearray(data3, "utf-8")) 
    # ~ ser.write(msg) 
    # ~ print("Wrote LOC Data Downstream")
    # ~ print("")
    
    TEST_API.sensor_token(b"SNSR",1)
    print("Requested SNS Data Upstream")
    TEST_API.decode_arrays()
    imu = TEST_API.get_array('IMU')
    print(imu)
    print("Received SNS Data Upstream")
    print("")
    
    counter += 1
    print(counter)
    # ~ time.sleep(.25)

proc1.close()
