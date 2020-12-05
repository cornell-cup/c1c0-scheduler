from r2_chatterbot.util import make_response
from r2_chatterbot.util import playtrack
from r2_chatterbot.util import path_planning
from r2_chatterbot.util import object_detection
from r2_chatterbot.util import face_recognition
from r2_chatterbot.util import utils
#from util.api import weather
#from util.api import restaurant
from playsound import playsound
import re
import sys
import os
from r2_chatterbot import corpus_and_adapter
import re

# for flask setup
import requests
import json
import io
import socket

from multiprocessing import Process
import subprocess
import os

# import C1C0-specific subsystems as available
import locomotion_cmd
# facial recognition

print(os.getcwd())
credential_path = "api_keys/speech_to_text.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

url = "http://18.216.143.187/"

utils.set_classpath()

def main():
    while True:
        #gets a tuple of phrase and confidence
        speech = input("Enter chatbot command: ")
        if "quit" in speech or "stop" in speech:
            break
        
        if("cico" in speech.lower() or "kiko" in speech.lower() or "c1c0" in speech.lower()):
            # filter out cico since it messes with location detection
            speech = utils.filter_cico(speech)
            if path_planning.isLocCommand(speech.lower()):
                cmd = path_planning.pathPlanning(speech.lower())
                # locomotion_cmd.chatbot_move(cmd)                     
                print("Move command (itemMove, direction, moveAmmount): ")
                print(path_planning.pathPlanning(speech.lower()))
                return cmd # don't worry, this only returns/exits the loop in the process handling locomotion
                               # chatbot main will get re-scheduled as soon as locomotion is handled
                # task is to transfer over to path planning on the system
            elif object_detection.isObjCommand(speech.lower()):
                #print("Object to pick up: " + object_detection.object_parse(speech.lower()))
                # run object detection `onjetson` - gets image of object facing C1C0's camera
                # this will run the object detection program in parallel as a separate process
                if not isloc: # only run if this is not a locomotion input
                    subprocess.Popen(['python3','objectdetection.py'])                
            else:
                # we don't want the text to be lowercase since it messes with location detection
                print(corpus_and_adapter.response_from_chatbot(speech))
                # send this element to AWS for response generation

                #begin the flask transfer now

if __name__ == '__main__':
    #playsound('sounds/cicoremix.mp3')
    main()
