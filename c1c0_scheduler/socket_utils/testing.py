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
scheduler_server.listen(2)

obj_det_client = socket.socket()
obj_det_client.connect(host_port)

chatbot_client = socket.socket()
chatbot_client.connect(host_port)

obj_det_client_conn, obj_det_client_addr = scheduler_server.accept()
chatbot_client_conn, chatbot_client_addr = scheduler_server.accept()

# Run test
while True:
    # Send chatbot msg
    start = time.time()
    # print('Chatbot:')
    to_object_detection(chatbot_client, 'botle')
    # print('Sending "botle".')
    # Scheduler forwards msg
    msg = chatbot_client_conn.recv(32)
    msg_str = msg.decode('UTF-8')
    sender = msg_str[0]
    transmitter = msg_str[2]  # le me
    receiver = msg_str[4]
    # print('Scheduler:')
    # print(f'Forwarding from {sender} to {receiver}.')
    if receiver == 'O':
        obj_det_client_conn.send(msg)
    else:
        pass
        # print('No receiver found.')

    # Receive chatbot's message
    # print('Object Detection:')
    print(from_chatbot(obj_det_client).decode('UTF-8'))
    # print('\n\n\n')
    print(time.time()-start)
    time.sleep(.01)
