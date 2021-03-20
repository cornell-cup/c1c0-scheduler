import socket
import os
import threading
import signal
from xbox360controller import Xbox360Controller

#concurrency primitives 
barrier = threading.Barrier(2) 

empty = threading.Semaphore(1)
full = threading.Semaphore(0)
#might not be necessary with just two threads will probably take it out
mutex = threading.Semaphore(1) 
producerData = ""
consumerResponse = ""

#DATA TYPES SUBJECT TO CHANGE
pathplanningData = ""
objectdetectionData = ""
locomotionData = "" #Possibly for feedback control
chatbotData = []



ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
threadlist = []
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def on_button_pressed(button):
	global threadlist
	global ThreadCount    
	print('Button {0} was pressed'.format(button.name))
	list_size = len(threadlist)
	for i in range(list_size):
		thread = threadlist.pop()		
		thread.do_run = False
		print("Thread was killed")
		ThreadCount -= 1

def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

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


def threaded_client(connection):
    global consumerResponse, producerData
    t = threading.currentThread()
    connection.send(str.encode('Welcome to the Server'))
    detectClient = True
    #Handshake Protocol
    while(getattr(t, "do_run", True) and detectClient):
        reply = ""
        data = connection.recv(2048)
        if(data.decode('utf-8') == "I am Chatbot"):
            reply = "Chatbot is recognized"
            client = "Chatbot"
            detectClient = False
            connection.sendall(str.encode(reply))
        elif(data.decode('utf-8') == "I am Producer"):
            reply = "Producer is recognized"
            client = "Producer"
            detectClient = False
            barrier.wait()
            connection.sendall(str.encode(reply))
        elif(data.decode('utf-8') == "I am Consumer"):
            reply = "Consumer is recognized"
            client = "Consumer"
            detectClient = False
            barrier.wait()
            connection.sendall(str.encode(reply))
        if not data:
            break
        
    #Commence Communication
    while(getattr(t, "do_run", True) and (not detectClient)):
        data = connection.recv(2048)
        if (client == "Chatbot"):
            reply = 'Server Says: ' + data.decode('utf-8')
            connection.sendall(str.encode(reply))
        elif (client == "Producer"):
            empty.acquire()
            mutex.acquire()
            producerData = data.decode('utf-8')
            if (consumerResponse == ""):
                reply = "Consumer has not responded yet"
            else:
                reply = consumerResponse
            mutex.release()  
            full.release()
            connection.sendall(str.encode(reply))
        elif (client == "Consumer"):
            full.acquire()
            mutex.acquire()
            consumerResponse = data.decode('utf-8')
            reply = producerData
            mutex.release()
            empty.release()
            connection.sendall(str.encode(reply))
        if not data:
            break
    
    connection.close()

t_xbox = threading.Thread(target=xboxcontroller, args=())
t_xbox.start()
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
