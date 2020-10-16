#pynput example (won't work with ssh)
"""
from pynput.keyboard import Key, Listener

def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    print('{0} released'.format(key))
    if key == Key.esc:
        return False #stop listener

with Listener(
    on_press = on_press,
    on_release=on_release) as listener:
    listener.join()
"""

import keyboard
import time

def key_press(key):
    print(key.name)

#keyboard.on_press(key_press)
"""
while True:
    time.sleep(0.05)
    if keyboard.is_pressed('esc'):
        raise KeyboardInterrupt
        time.sleep(0.05)
"""
    #raise Exception
def run(distance):
    keyboard.on_press(key_press)
    while not keyboard.is_pressed('down'):
        time.sleep(0.1)
        degree = 0
        x = 0
        y = 0

        if keyboard.is_pressed('right'):
            degree = 1
        if keyboard.is_pressed('left'):
            degree = -1
        if keyboard.is_pressed('a'):
            x -= 1
        if keyboard.is_pressed('d'):
            x += 1
        if keyboard.is_pressed('w'):
            y += 1
        if keyboard.is_pressed('d'):
            y -= 1
        #motorcommand(x,y)
        #headcommand(degree)
        #print("x = %d y = %d" % (x,y))
    keyboard.press('esc')
    keyboard.release('esc')
run(0)
#Original Code
"""
def run(distance):
    joy = xbox.Joystick()
    while not joy.Back():
        time.sleep(0.1)
        degree = 0
        x = 0
        y = 0

        if joy.rightTrigger() > 0:
            degree = 1;
        if joy.leftTrigger() > 0:
            degree = -1
        x = joy.leftX()
        y = joy.leftY()
        motorcommand(x ,y)
        headcommand(degree)
"""
