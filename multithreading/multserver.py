import socket
import os
import threading
import signal
from xbox360controller import Xbox360Controller
import serial
import sys
from contextlib import contextmanager
import subprocess
sys.path.append('~/Desktop/c1c0-modules/c1c0-movement/c1c0-movement/Locomotion') #Relative to THIS directory (multithreading)
import R2Protocol2 as r2p
import locomotion_API
import arm_API
from xboxcontrol_API import xboxcontroller
import HeadRotation_XBox_API as headrotation
import strongarm_API as strongarm

# from dotenv import load_dotenv

# load_dotenv()

# # Serial Data thread that collects data and updates global dictionaries
# # Alternate method: have data updated locally on the sensor microcontroller;
# #                   the server actively polling the data when needed
# t_serialdata = threading.Thread(target=serialdata, args=())
# t_serialdata.start()

# # for xbox control: kill all thread except chatbot
# def on_button_pressed(button):
    # global threadlist
    # global ThreadCount
    # global chatbotThread    
    # print('Button {0} was pressed'.format(button.name))
    # list_size = len(threadlist)
    # for i in range(list_size):
        # thread = threadlist.pop()
        # if (thread != chatbotThread):		
            # thread.do_run = False
            # print("Thread was killed")
            # ThreadCount -= 1

# # for xbox control
# def on_button_released(button):
    # print('Button {0} was released'.format(button.name))

# # for xbox control
# def on_axis_moved(axis):
    # # TODO send command to locomotion to control the head rotatioon
    # print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

# # give function handlers to xbox controller package
# def xboxcontroller():
        # try:
                # with Xbox360Controller(0, axis_threshold=0.2) as controller:
                        # # Button A events
                        # controller.button_a.when_pressed = on_button_pressed
                        # controller.button_a.when_released = on_button_released

                        # # Left and right axis move event
                        # controller.axis_l.when_moved = on_axis_moved
                        # controller.axis_r.when_moved = on_axis_moved

                        # signal.pause()
        # except KeyboardInterrupt:
                # pass

# # read serial data, store in Data['terabee1']
# # TODO template for all sensor data reading
# # right now serves as the main function of a thread to collect data and update dictionary
# def serialdata():
    # try:
        # while True:
            # s = ser.read(32) #reads serial buffer for terabee
            # Data['terabee1'] = "" #clears previous values
            # mtype, msg, status = r2p.decode(s) #decodes serial message (see R2Protocol2.py)
            # if(status == 1):
                # for i in range(len(msg)): #loop through length of data
                    # if i % 2 == 0:
                        # Data['terabee1'] += str(msg[i]) + str(msg[i+1]) + "," #assemble char values into int16s and put them in Data dictionary as a string
    # except KeyboardInterrupt:
        # ser.close()


def kill_thread(client):
    """
    Function for halting a process thread when its work is done
    Used in conjunction with socket closing inside the client API
    """
    global threadlist
    global ThreadCount
    for thread in threadlist:
        if thread.getName() == client:
            thread.do_run = False
            threadlist.remove(thread)
            ThreadCount -= 1

def threaded_client(connection):
    """
    Function to initialize a software subprocess as a thread,
    handshake with the scheduler, and process requests from processes 
    """
    global chatbotThread
    t = threading.currentThread()
    connection.send(str.encode('Welcome to the Server'))
    detectClient = True
    # Handshake Protocol
    while(getattr(t, "do_run", True) and detectClient):
        reply = ""
        data = connection.recv(2048)
        if(data.decode('utf-8') == "I am xboxcontroller"):
            xboxcontrollerThread = t
            reply = "xboxcontroller is recognized"
            client = "xboxcontroller"
            detectClient = False
            connection.sendall(str.encode(reply))
        elif(data.decode('utf-8') == "I am Chatbot"):
            chatbotThread = t
            reply = "Chatbot is recognized"
            client = "Chatbot"
            detectClient = False
            connection.sendall(str.encode(reply))
        elif(data.decode('utf-8') == "I am path-planning"):
            reply = "path-planning is recognized"
            client = "path-planning"
            detectClient = False
            connection.sendall(str.encode(reply))
        elif(data.decode('utf-8') == "I am object-detection"):
            reply = "object-detection is recognized"
            client = "object-detection"
            detectClient = False
            connection.sendall(str.encode(reply))
        elif(data.decode('utf-8') == "I am facial-recognition"):
            reply = "facial-recognition is recognized"
            client = "facial-recognition"
            detectClient = False
            connection.sendall(str.encode(reply))
        elif not data:
            break
    t.setName(client)

    #Commence Communication
    while(getattr(t, "do_run", True) and (not detectClient)):
        data = connection.recv(2048)
        if(data.decode('utf-8') == "kill"):
            kill_thread(client)
        if (client == "Chatbot"):
            if ("path-planning" in data.decode('utf-8')):
                reply = "path-planning started with arguments"
                argument = data.decode('utf-8')[14:]
                # print("this is pathplanning argument -- " + argument)
                connection.sendall(str.encode(reply))
                pid = subprocess.Popen([sys.executable, os.getenv('PATH_PLANNING'), argument]) #"client_pathplanning.py" "/home/cornellcup-cs-jetson/Desktop/c1c0-modules/C1C0_path_planning/Jetson.py"
            elif ("object-detection" in data.decode('utf-8')):
                reply = "object-detection started with arguments"
                argument = data.decode('utf-8')[36:]
                print("data: " + data.decode('utf-8'))
                print("argument: " + argument) 
                connection.sendall(str.encode(reply))
                pid = subprocess.Popen([sys.executable, os.getenv('OBJECT_DETECTION'), argument]) #"client_objectdetection.py" "/home/cornellcup-cs-jetson/Desktop/c1c0-modules/r2-object_detection/scheduler_test.py"
            elif ("attendance" in data.decode('utf-8')):
                reply = "facial-recognition started"
                print("data: " + data.decode('utf-8'))
                connection.sendall(str.encode(reply))
                pid = subprocess.Popen([sys.executable, "-m", os.getenv('FACIAL_RECOGNITION')], env={'PYTHONPATH':os.getenv('FACIAL_RECOGNITION_PATH')})
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
                '''
        elif (client == "xboxcontroller"):
            if ("xbox" in data.decode('utf-8')):
                reply = "xboxcontroller signal: " + data.decode('utf-8')[6:]
                connection.sendall(str.encode(reply))
                '''
        elif (client == "xboxcontroller"):
            if ("xbox" in data.decode('utf-8')):
                print("-------------------------------hello-----------------------")
                #print(data)
                #print(data.decode('utf-8')[6:])
                reply = "xboxcontroller signal: " + data.decode('utf-8')[6:] + " sent to arduino"
                locomotion_API.locomotion_msg('/dev/ttyTHS1', 115200, data.decode('utf-8')[6:]) # serial port: /dev/ttyTHS1 USB port: /dev/ttyACM0
                connection.sendall(str.encode(reply))
            elif("head" in data.decode('utf-8')):
                print("-------------------------------hiii-----------------------")
                #print(data)
                #print(data.decode('utf-8'))
                reply = "xboxcontroller signal: " + data.decode('utf-8') + " sent to arduino"
                headrotation.head_msg('/dev/ttyTHS1', 115200, data.decode('utf-8')) # serial port: /dev/ttyTHS1 USB port: /dev/ttyACM0
                connection.sendall(str.encode(reply))
            elif("strong" in data.decode('utf-8')):
                print("-------------------------------strong-----------------------")
                print(data)
                reply = "xboxcontroller signal: " + data.decode('utf-8') + " sent to arduino"
                strongarm.strong_msg('/dev/ttyTHS1', 9600, data.decode('utf-8'))
                connection.sendall(str.encode(reply))
                
        elif (client == "path-planning"):
            if ("locomotion" in data.decode('utf-8')):
                motor_power = data.decode('utf-8')[11:]
                print(motor_power)
                locomotion_API.locomotion_msg('/dev/ttyTHS1', 115200, motor_power) # serial port: /dev/ttyTHS1 USB port: /dev/ttyACM0
                reply = "motor power command sent to locomotion"
                connection.sendall(str.encode(reply))
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
        elif (client == "object-detection"):
            if ("arm" in data.decode('utf-8')):
                reply = ""
                arm_angle = data.decode('utf-8')[4:]
                print(arm_angle)
                arm_API.arm_msg('/dev/ttyTHS1', 115200, arm_angle)
                reply = "arm angle command sent to precision arm"
                connection.sendall(str.encode(reply))

                #if (Data_lock["terabee1"].acquire(blocking=False)):
                #    print(str(t.ident) + " got the lock!!!!")
                #    reply = "Server data request: " + Data["terabee1"]
                #    Data_lock["terabee1"].release()
                #else:                                      
                #    reply = "Could not acquire lock"
                #connection.sendall(str.encode(reply))
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
        elif (client == "facial-recognition"):
            if ("found" in data.decode('utf-8')):
                people = data.decode('utf-8')[6:]
                print(people)
                # locomotion_API.locomotion_msg('/dev/ttyTHS1', 115200, motor_power) # serial port: /dev/ttyTHS1 USB port: /dev/ttyACM0
                # in place of the line above, need to implement a chatbot API that can receive commands or something
                reply = "facial recognition results sent to chatbot"
                connection.sendall(str.encode(reply))
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
        if not data:
            break

    connection.close()

# ser = serial.Serial(
#         port = '/dev/ttyTHS1',
#         baudrate = 115200,
#         )
# ser.close()
# ser.open()

ServerSocket = socket.socket()
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '127.0.0.1'
port = 1233
ThreadCount = 0
threadlist = []
chatbotThread = None
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

xboxThread = threading.Thread(target=xboxcontroller, args=( ))
xboxThread.start()
# TODO start chatbot thread
# subprocess.Popen([sys.executable, "-m", "r2_facial_recognition.client"], env={'PYTHONPATH':'/home/cornellcupcs/Desktop/c1c0_modules/r2-facial_recognition_client'})
# subprocess.Popen([sys.executable, os.getenv('CHATBOT')])
#Chatbot needs to be created and not killed, or if it gets killed, it needs to be immediately restarted (or sleep it)
while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    t1 = threading.Thread(target=threaded_client, args=(Client, ))
    t1.start()
    threadlist.append(t1)
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
