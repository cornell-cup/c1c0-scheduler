# chatbot <--> scheduler 

# 1. spawn pathplanning (path planning will talk to locomotion)

# 2. spawn object detection (object detection will return the direction result)
# 2.1 spawn pathplanning (path planning will talk to locomotion)

# 3. spawn object detection (object detection will talk to arm directly)


#!/usr/bin/env python3

from threading import Lock
import socket

lock = Lock()  # for function thread
flag = 0  # for xbox controller

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def main_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                # if flag = 1:
                # 	kill thread
                # else if lock grabbed:
                # 	conn.sendall("resource occupied")
                # else:
                # 	spawn pathplanning or object detection as a thread
                # 		thread will grab the lock, spawn the program,
                #       waiting for result to come back, release lock,
                #       return result


def function_thread(program, data):
    lock.acquire()
    result = program(data)
    # FIXME: What is the value of `termination`?
    # if result != termination:
        # call pathplanning
        # result = pathplanning(result)
    lock.release()
    return result


def xbox_thread():
    pass
    # waiting for interrupt
    # kill function_thread (stop flag, release the lock if lock is grabbed)
    # do whatever it is going to do
    # flip the thread back to 0
