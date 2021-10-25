import socket
from chatbot import to_object_detection
from object_detection import from_chatbot
import time
# Establish scheduler server

host, port = host_port = '127.0.0.1', 1233

scheduler_server = socket.socket()

try:
    scheduler_server.bind(host_port)
except socket.error as e:
    print(str(e))
print('Scheduler server started')
time.sleep(1)
print('Attempting to connect')


# Establish clientele

obj_det_client = socket.socket()
obj_det_client.connect(host_port)

chatbot_client = socket.socket()
chatbot_client.connect(host_port)


# Run test
while True:
    # Send chatbot msg
    print('Chatbot:')
    to_object_detection(chatbot_client, 'botle')
    print('Sending "botle".')
    # Scheduler forwards msg
    msg = scheduler_server.recv(32)
    sender = msg[0]
    transmitter = msg[2]  # le me
    receiver = msg[4]
    print('Scheduler:')
    print(f'Forwarding from {sender} to {receiver}.')
    if receiver == 'O':
        scheduler_server.send(msg)
    else:
        print('No receiver found.')

    # Receive chatbot's message
    print('Object Detection:')
    print(from_chatbot(obj_det_client))
    time.sleep(1)
