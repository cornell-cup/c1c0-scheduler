#Test of Jetson External Interrupts
#incorporates NVIDIA Jetson GPIO library
#https://github.com/NVIDIA/jetson-gpio


#Add external interrupt on Jetson pin 18
import Jetson.GPIO as GPIO
import time

def interrupted(channel):
    print("interrupt")

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.IN)
    GPIO.add_event_detect(18, GPIO.FALLING, callback = interrupted)
    print("starting")

    while True:
        for i in range(1000000):
            if i == 10:
                print("running")

if __name__ == '__main__':
    main()
