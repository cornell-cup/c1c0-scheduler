import socket
import threading
import signal
import subprocess
import os

import serial
from xbox360controller import Xbox360Controller

from c1c0_movement.Locomotion import R2Protocol2 as r2p

from config import (
    DEFAULT_HOST, DEFAULT_PORT, ENCODING, extract_process_type, ProcessTypes,
    letter_process_map, cmd_digest, PRIMARY_PROCESS
)


# Defining all the functions used first before running script


# for xbox control: kill all thread except chatbot
def on_button_pressed(button):
    global thread_list
    global thread_count
    global primary_thread
    print(f'Button {button.name} was pressed')
    list_size = len(thread_list)
    for i in range(list_size):
        thread = thread_list.pop()
        if thread != primary_thread:
            thread.do_run = False
            print("Thread was killed")
            thread_count -= 1


# for xbox control
def on_button_released(button):
    print(f'Button {button.name} was released')


# for xbox control
def on_axis_moved(axis):
    # TODO send command to locomotion to control the head rotation
    print(f'Axis {axis.name} moved to {axis.x} {axis.y}')


# give function handlers to xbox controller package
def xbox_controller():
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
# right now serves as the main function of a thread to collect data and update
#  dictionary
def serial_data():
    try:
        while True:
            s = ser.read(32)  # reads serial buffer for terabee
            Data['terabee1'] = ""  # clears previous values
            # decodes serial message (see R2Protocol2.py)
            mtype, msg, status = r2p.decode(s)
            if status == 1:
                for i in range(len(msg)):  # loop through length of data
                    if i % 2 == 0:
                        Data['terabee1'] += str(msg[i]) + str(msg[i + 1]) + ","
                        # assemble char values into int16s and put them in
                        #  Data dictionary as a string
    # FIXME: Shouldn't this just be a finally block?
    except KeyboardInterrupt:
        ser.close()


def kill_thread(client):
    """
    Function for halting a process thread when its work is done
    Used in conjunction with socket closing inside the client API
    """
    global thread_list
    global thread_count
    for thread in thread_list:
        if thread.getName() == client:
            thread.do_run = False
            thread_list.remove(thread)
            thread_count -= 1


def threaded_client(connection: socket.socket):
    # global consumerResponse, producerData
    global primary_thread
    t = threading.currentThread()
    connection.sendall('Welcome to the Server'.encode(ENCODING))
    # Handshake Protocol
    reply = ""
    client = None
    while getattr(t, "do_run", True):
        data = connection.recv(2048)
        data_decoded = data.decode(ENCODING)
        try:
            client = extract_process_type(data_decoded)
            if client is PRIMARY_PROCESS:
                primary_thread = t
            reply = f'{client} is recognized.'
            break
        except ValueError:
            reply = 'MalformedMessage'
        if not data:
            break
    connection.sendall(reply.encode(ENCODING))
    if client is None:
        # TODO: Something, return/cleanup maybe
        pass

    t.name = client
    # Commence Communication
    while getattr(t, "do_run", True):
        data = connection.recv(2048)
        data_decoded = data.decode(ENCODING)
        if data_decoded == "kill":
            kill_thread(client)

        sender, _, receiver, body = cmd_digest(data_decoded)
        sender = letter_process_map[sender]
        receiver = letter_process_map[receiver]
        cmds = sender.value[1]
        result = None
        for cmd_name, cmd in cmds.items():
            if body.startswith(cmd_name):
                result = cmd(connection, sender.value[0], receiver.value[0])
                break
        if result is None:
            # No commands ran (presumably)
            pass
        if not data:
            break

    connection.close()


Data = {
    "terabee1": "",
    "terabee2": "",
    "terabee3": "",
    "lidar": "",
    "imu": "",
}

Data_lock = {
    "terabee1": threading.Lock(),
    "terabee2": threading.Lock(),
    "terabee3": threading.Lock(),
    "lidar": threading.Lock(),
    "imu": threading.Lock(),
}

# Why close then open?
ser = serial.Serial(port='/dev/ttyTHS1', baudrate=115200)
ser.close()
ser.open()


# TODO: Refactor these functions into files imported by `config.py`
#  or something
def start(conn, _, receiver):

    conn.sendall(f'{receiver} started with arguments'.encode(ENCODING))
    return subprocess.Popen([
        os.path.join('.', 'shells', 'start.sh'), receiver
    ])


def get_terabee_data(conn, _, __):
    if Data_lock["terabee1"].acquire(blocking=False):
        reply = "Server data request: " + Data["terabee1"]
        Data_lock["terabee1"].release()
    else:
        reply = "Could not acquire lock"
    conn.sendall(str.encode(reply))


# Configure module behaviors
ProcessTypes.CHATBOT.value[1]['start'] = start
ProcessTypes.PATH_PLANNING.value[1]['get_data'] = get_terabee_data


ServerSocket = socket.socket()
host = DEFAULT_HOST
port = DEFAULT_PORT
thread_count = 0
thread_list = []
primary_thread = None
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

# Serial Data thread that collects data and updates global dictionaries
# Alternate method: have data updated locally on the sensor microcontroller;
#                   the server actively polling the data when needed
t_serialdata = threading.Thread(target=serial_data, args=())
t_serialdata.start()


t_xbox = threading.Thread(target=xbox_controller, args=())
t_xbox.start()

# TODO start chatbot thread 

# Chatbot needs to be created and not killed, or if it gets killed, it needs
#  to be immediately restarted (or sleep it)
try:

    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ': ' + str(address[1]))
        t1 = threading.Thread(target=threaded_client, args=(Client, ))
        t1.start()
        thread_list.append(t1)
        thread_count += 1
        print('Thread Number: ' + str(thread_count))
finally:
    ServerSocket.close()
