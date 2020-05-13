# Locomotion Multithreading Proof of Concept

import threading
from threading import Lock
import time
import random
import sys

lock = Lock()  # prevent multiple processesing from accessing locomotion resource


def chat_funct():
    '''
    Called by main_thread()
    Returns: 
        value - random int
        loco - 1 or 0 based on value
    '''
    value = random.randint(0, 6)
    loco = 1 if value > 3 else 0
    return loco, value


def child_thread(sleep_time):
    '''
    Called by main_thread()
    Acquires lock and does work for sleep_time amount.
    '''
    lock.acquire()
    print('Child thread received chat bot command. Value: ' + str(sleep_time))
    for i in range(0, sleep_time):
        time.sleep(1)
        print('Child thread doing work:' + str(i) + ' seconds')
    print('Child thread finished.')
    lock.release()


def main_thread():
    '''
    Runs main thread infinitely.
    Calls chat_funct() every iteration. If chat_funct() generates a locomotion 
    command, create child thread. Prevent the main thread from running until
    child thread runs to completion. 
    '''
    lock.acquire()
    i = 0
    while(1):
        print('Main thread iteration number:' + str(i))
        i += 1
        locomotion, value = chat_funct()
        if (locomotion):
            lock.release()
            blocking_thread = threading.Thread(
                target=child_thread, args=(value,))  # create child thread
            blocking_thread.start()
            blocking_thread.join()
            lock.acquire()
        time.sleep(1)

    print('Main thread finished.')
    lock.release()


if __name__ == '__main__':

    t1 = threading.Thread(target=main_thread)

    t1.start()  # start main thread
