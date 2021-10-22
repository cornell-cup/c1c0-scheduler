import socket
import os
import threading
import signal
from xbox360controller import Xbox360Controller
import serial
import sys
from contextlib import contextmanager
import subprocess
import sys

Data = {
    "terabee1" : "",
    "terabee2" : "",
    "terabee3" : "",
    "lidar" : "",
    "imu" : "",
}

Data_lock = {
    "terabee1" : threading.Lock(),
    "terabee2" : threading.Lock(),
    "terabee3" : threading.Lock(),
    "lidar" : threading.Lock(),
    "imu" : threading.Lock(),
}


sys.path.append('../../c1c0-movement/c1c0-movement/Locomotion') #Relative to THIS directory (multithreading)
import R2Protocol2 as r2p

ser = serial.Serial(
	port = '/dev/ttyTHS1',
	baudrate = 115200,
)
ser.close()
ser.open()

# #concurrency primitives 
# barrier = threading.Barrier(2) 

# empty = threading.Semaphore(1)
# full = threading.Semaphore(0)
# #might not be necessary with just two threads will probably take it out
# mutex = threading.Semaphore(1) 
# producerData = ""
# consumerResponse = ""


# @contextmanager
# def non_blocking_lock(lock=threading.Lock()):
#     if not lock.acquire(blocking=False):
#         raise WouldBlockError
#     try:
#         yield lock
#     finally:
#         lock.release()

ServerSocket = socket.socket()
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

# for xbox control: kill all thread except chatbot
def on_button_pressed(button):
    global threadlist
    global ThreadCount
    global chatbotThread    
    print('Button {0} was pressed'.format(button.name))
    list_size = len(threadlist)
    for i in range(list_size):
        thread = threadlist.pop()
        if (thread != chatbotThread):		
            thread.do_run = False
            print("Thread was killed")
            ThreadCount -= 1

# for xbox control
def on_button_released(button):
    print('Button {0} was released'.format(button.name))

# for xbox control
def on_axis_moved(axis):
    # TODO send command to locomotion to control the head rotatioon
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

# give function handlers to xbox controller package
def xboxcontroller():
	try:
		with Xbox360Controller(0, axis_threshold=0.2) as controller:
			# Button A events
			controller.button_a.when_pressed = on_button_pressed
			controller.button_a.when_released = on_button_released

			# Left and right axis move event
			controller.axis_l.when_moved = on_axis_moved
			controller.axis_r.when_moved = on_axis_moved

			signal.pause()
	except KeyboardInterrupt:
		pass

# read serial data, store in Data['terabee1']
# TODO template for all sensor data reading
# right now serves as the main function of a thread to collect data and update dictionary
def serialdata():
    try:
        while True:
            s = ser.read(32) #reads serial buffer for terabee
            Data['terabee1'] = "" #clears previous values
            mtype, msg, status = r2p.decode(s) #decodes serial message (see R2Protocol2.py)
            if(status == 1):
                for i in range(len(msg)): #loop through length of data
                    if i % 2 == 0:
                        Data['terabee1'] += str(msg[i]) + str(msg[i+1]) + "," #assemble char values into int16s and put them in Data dictionary as a string
    except KeyboardInterrupt:
        ser.close()

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
    # global consumerResponse, producerData
    global chatbotThread
    t = threading.currentThread()
    connection.send(str.encode('Welcome to the Server'))
    detectClient = True
    #Handshake Protocol
    while(getattr(t, "do_run", True) and detectClient):
        reply = ""
        data = connection.recv(2048)
        if(data.decode('utf-8') == "I am Chatbot"):
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
        # elif(data.decode('utf-8') == "I am Producer"):
        #     reply = "Producer is recognized"
        #     client = "Producer"
        #     detectClient = False
        #     barrier.wait()
        #     connection.sendall(str.encode(reply))
        # elif(data.decode('utf-8') == "I am Consumer"):
        #     reply = "Consumer is recognized"
        #     client = "Consumer"
        #     detectClient = False
        #     barrier.wait()
        #     connection.sendall(str.encode(reply))
        if not data:
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
                connection.sendall(str.encode(reply))
                pid = subprocess.Popen([sys.executable, "client_pathplanning.py", argument])
            elif ("object-detection" in data.decode('utf-8')):
                reply = "object-detection started"
                argument = data.decode('utf-8')[17:]
                connection.sendall(str.encode(reply))
                pid = subprocess.Popen([sys.executable, "client_objectdetection.py", argument]) 
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
            
        elif (client == "path-planning"):
            if (data.decode('utf-8') == "get data"):
                reply = ""
                if (Data_lock["terabee1"].acquire(blocking=False)):
                    print(str(t.ident) + " got the lock!!!!")
                    reply = "Server data request: " + Data["terabee1"]
                    Data_lock["terabee1"].release()
                else:
                    reply = "Could not acquire lock"
                connection.sendall(str.encode(reply))
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
        elif (client == "object-detection"):
            if (data.decode('utf-8') == "get data"):
                reply = ""
                if (Data_lock["terabee1"].acquire(blocking=False)):
                    print(str(t.ident) + " got the lock!!!!")
                    reply = "Server data request: " + Data["terabee1"]
                    Data_lock["terabee1"].release()
                else:
                    reply = "Could not acquire lock"
                connection.sendall(str.encode(reply))
            else:
                reply = 'Server Says: ' + data.decode('utf-8')
                connection.sendall(str.encode(reply))
        # elif (client == "Producer"):
        #     empty.acquire()
        #     mutex.acquire()
        #     producerData = data.decode('utf-8')
        #     if (consumerResponse == ""):
        #         reply = "Consumer has not responded yet"
        #     else:
        #         reply = consumerResponse
        #     mutex.release()  
        #     full.release()
        #     connection.sendall(str.encode(reply))
        # elif (client == "Consumer"):
        #     full.acquire()
        #     mutex.acquire()
        #     consumerResponse = data.decode('utf-8')
        #     reply = producerData
        #     mutex.release()
        #     empty.release()
        #     connection.sendall(str.encode(reply))
        if not data:
            break
    
    connection.close()


# Serial Data thread that collects data and updates global dictionaries
# Alternate method: have data updated locally on the sensor microcontroller;
#                   the server actively polling the data when needed
t_serialdata = threading.Thread(target=serialdata, args=())
t_serialdata.start()


t_xbox = threading.Thread(target=xboxcontroller, args=())
t_xbox.start()

# TODO start chatbot thread 

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
