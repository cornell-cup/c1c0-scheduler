# This Client Program
# Voice triggered
# Get image from Pi, send it to computing server by using POST
# Receive json feedback from server
# Make robot react to parsed json

import json
import requests
import sys
import io
import socket
import picamera
import face_recognition
from PIL import Image
from num2words import num2words
from subprocess import call
import subprocess
#import robot_control

# find largest face in the image
# return None if no face is found or the face is too small
# (less than 1/12 of the image)
def find_face(image):

    face_locations = face_recognition.face_locations(image)
    """
    for face_location in face_locations:
        top, right, bottom, left = face_location
        image_x, image_y, d = image.shape
        # minimal threshold to reject a face result if face too small
        threshold = min(image_x, image_y) / 12
        if right - left > threshold:
            # a qualifying face
            return face_location
    """
    if len(face_locations) > 0:
        return face_locations[0]

    return None

url = "http://10.129.19.162:11000/"

def send_test_image():
    files = {
        "image": open("cropped.png", "rb")
    }
    response = requests.post(url + "identify-face", files=files, verify=False)
    return response.json()

#get the check in result from the json and return the reuslt
def JsonLoad(CheckInData):
    #temp = json.load(CheckInData)
    temp = CheckInData
    person = temp['name']
    checkInStatus = temp['checkInStatus']
    meetingType = temp['meetingType']
    return person, checkInStatus, meetingType


#speak the check in result using
def speakResult(person, checkInStatus, meetingType):
    if person == 'None' or person == None:
        text = 'No such a person and person is none'
    else:
        text = person + 'successfully check in'
    subprocess.check_output(['espeak','-ven-us', text])


def DetectFace():
    # capture image
    failure_tries = 0
    camera = picamera.PiCamera()
    camera.resolution = (960, 540)
    while failure_tries < 3:
        image = camera.capture("capture.png")
        image = face_recognition.load_image_file("capture.png")
        face_location = find_face(image)
        if face_location != None:
            top, right, bottom, left = face_location
            # check if the face is within the middle 20% of the image
            face_center = (right + left) / 2
            image_x, image_y, d = image.shape
            if face_center > image_y * 0.2 and face_center < image_y * 0.8:
                # crop image

                top = top - min(100, bottom)
                bottom = bottom + min(100, image_x - top)
                left = left - min(100, left)
                right = right + min(100, image_y - right)

                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                pil_image.save('cropped.png', 'PNG')

                camera.close()
                return True
        else:
            # shake head and say i cannot find you
            subprocess.check_output(['espeak','-ven-us', 'I cannot see your face'])
            failure_tries += 1
    camera.close()
    return False

def writeResultToFile(text):
    with open('FacialRecognitionResult.txt', 'w') as f:
        f.write(text)

def CheckIn():
    # detected a valid face
    if DetectFace():
        subprocess.check_output(['espeak','-ven-us', 'I saw your face'])

        print("detected a valid face")
        json_feedback = send_test_image()
        person, checkInStatus, meetingType = JsonLoad(json_feedback)
        print(person, checkInStatus, meetingType)
        speakResult(person, checkInStatus, meetingType)
        
        text = ''
        text += 'person: ' + str(person) + '\n'
        text += 'checkInStatus: ' + str(checkInStatus) + '\n'
        text += 'meetingType: ' + str(meetingType)
        writeResultToFile(text)
        
    else:
        print("cannot detect a valid face")
        subprocess.check_output(['espeak','-ven-us', 'I cannot see your face'])


# name should be the parameter to be passed in
def MakeFriend(name):

    if DetectFace():
        print("detected a valid face")
        files = {
            "image": open("cropped.png", "rb")
        }
        data = {
            "name": name
        }
        response = requests.post(url + "save-face", files=files, data=data, verify=False)

        if response.status_code == 422:
            print('Face exists')
            text = 'I already know you'
        elif response.status_code == 200:
            print('Add friend successful')
            text = 'I added you as ' + name
        else:
            print('I cannot add you as friend')
            text = 'I cannot add you as friend'

        subprocess.check_output(['espeak', '-ven-us', text])
        writeResultToFile(text)
        
    else:
        print("cannot detect a valid face")
        subprocess.check_output(['espeak','-ven-us', 'I cannot see your face'])

#CheckIn()
