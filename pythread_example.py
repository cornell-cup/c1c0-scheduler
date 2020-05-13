# pythread example
# sample functionality for a multithreaded program

import threading
from threading import Lock
import time
import random
import sys

'''
1. Have main thread 
'''

lock = Lock()


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

# no-argument function that sleeps for a random amount of time
# between 2 and 5 seconds before finishing, printing each second


def main_thread():
    '''
    Runs main thread infinitely.
    Calls chat_funct() every iteration. If chat_funct() generates a locomotion 
    command, create child thread. Prevent the main thread from running until
    child thread runs to completion. 
    '''
    lock.acquire()
    #sleep_time = int(5*random.random()+2)
    i = 0
    while(1):
        print('Main thread iteration number:' + str(i))
        i += 1
        #locomotion, value = chat_funct()
        chat_thread = threading.Thread(target=chat_funct)
        chat_thread.start()
        locomotion, value = chat_thread.join()

        if (locomotion):
            lock.release()
            blocking_thread = threading.Thread(
                target=child_thread, args=(value,))
            blocking_thread.start()
            blocking_thread.join()
            lock.acquire()
        time.sleep(1)

    print('Main thread finished.')
    lock.release()


# the above two functions will run in parallel in two threads. Keep in mind
# that threads exist in the same process, with the same memory space and stack,
# but run in parallel based on Python's threading API (which itself is based on
# POSIX threads in C)
# the next step is to initialize thread objects for each function - this lets the system
# keep track of where each function exists so it can switch between them

if __name__ == '__main__':

    #main_t = threading.Thread(target=main_thread_function)
    # main_t.start()

    # this one just needs the function name,
    t1 = threading.Thread(target=main_thread)
    # since it has no arguments

    # the argument `args` are the
    #t2 = threading.Thread(target=sleepy_time, args=(3,))
    # arguments you would pass into the
    # function if you were calling it normally

    # with each of the threads created, now we can start running them

    t1.start()
    # t2.start()

    # t2.join()
    # when you run this program (i've been doing it from a linux command line),
    # you'll see output coming from each thread concurrently. This program outlines
    # the fundamentals of a multithreaded program - two functions, which can take
    # arguments, run in parallel to completion, and disappear when they're done

    # because neither thread has any shared memory, concurrency isn't an issue - so there
    # is no need for locks or semaphores or condition variables or anything.

    # the threading API has a lot more functionality - threads can exit, block each other, join
    # back to other threads - all things that you might find useful when writing. Explore the
    # documentation when you can.
