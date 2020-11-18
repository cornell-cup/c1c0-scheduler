# scheduler.py
# Top-level process management for all C1C0 subsystems
# Written by Brett Sawka, May 2020
# Based on pythread_example.py by Jackie Woo

# NOTE: This program MUST, MUST, MUST be run from the command line.
# This process will have a low parent id, while the spawned child process
# will have a high parent id. This will allow for the correct process management.

# Another NOTE: this is yet to be tested. Changes are inevitable.

# For further clarifications, read the section about the scheduler in the C1C0 Spring 2020 documentation
# Feel free to contact Brett Sawka (bas335@cornell.edu) with questions

import threading
from threading import Lock
import time
import random
import sys
from multiprocessing import Process
import r2_chatterbot # pull from the scheduling branch of the chatbot repo and pip3 install
                     # python3 setup.py sdist
                     # pip3 install ./dist/r2_chatterbot-1.0.tar.gz
from r2_chatterbot.main import main

import locomotion_cmd
from c1c0_locomotion import locomotion # pull from the scheduling branch of demolocomotion repo
                                       # use same commands as above, but replace r2_chatterbot with c1c0_locomotion

lock = Lock()  # prevent multiple processesing from accessing locomotion resource

def chatbot_thread():
    '''
    Starts a parallel chatbot specifically for getting locomotion commands
    '''
    while True: # restart chatbot once locomotion is finished
        cmd = r2_chatterbot.main.main(isloc=True) # runs until a chatbot command happens
        if cmd[1] != -500 and cmd[2] != -500: # (-500,-500) is the chatbot locomotion default - essentially means no command
            lock.acquire() # begin critical section
            locomotion_cmd.chatbot_move(cmd) # actuate locomotion motors
            print('finished chatbot movement')
            lock.release()

def main_thread():
    '''
    Runs main thread infinitely.
    Constantly takes xbox controller input and calls a motor command using controller input
    within a critical section
    '''
    while True:
        print("Heeeeeeelllooo")
        time.sleep(0.1) # assure commands complete
        motor_cmd = locomotion.get_xbox() # get xbox input

        lock.acquire() # critical section begin
        # locomotion.run_single_command(motor_cmd) # actuate motors for movement
        print("Running motor command at"+ str(motor_cmd))
        lock.release() # critical section end


if __name__ == '__main__':
#    target = r2_chatterbot.main.main()
#    p = Process(target) # start child process to handle chatbot input for non-locomotion systems
   # p.start() # process will run in parallel, and will not interfere with locomotion
    t1 = threading.Thread(target=main_thread)
#    t2 = threading.Thread(target=chatbot_thread)

    t1.start()  # start main thread
#    t2.start()  # start chatbot thread
