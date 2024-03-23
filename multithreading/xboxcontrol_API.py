from xbox360controller import Xbox360Controller
import signal
import time
import client
import HeadRotation_XBox_API as hR
import Locomotion_API as loco
import strongarm_API as strong
import arm_API as precise
from playsound import playsound
import random

r2d2sounds = []
for i in range(1,6):
    r2d2sounds.append('/home/cornellcup/c1c0-main/c1c0-scheduling/multithreading/r2d2sounds/r2d2-'+str(i)+'.mp3')

# for xbox control
def on_button_held(button):

    if(button.name == 'button_a'):
        scheduler.communicate(strong.move_shoulder(1))
    if(button.name == 'button_b'):
        #scheduler.communicate('xbox: (+0.00,+0.00)')
        scheduler.communicate(strong.move_shoulder(2))

last_axis = {}
def on_axis_moved(axis):
    global last_axis
    time.sleep(.01)
    axis_threshold = .5
    if(axis.x <= -axis_threshold):
        axis_x = -1
    elif(axis.x >= axis_threshold):
        axis_x = 1
    else:
        axis_x = 0
    if(axis.y <= -axis_threshold):
        axis_y = 1
    elif(axis.y >= axis_threshold):
        axis_y = -1
    else:
        axis_y = 0
    if(axis.name not in last_axis):
        last_axis[axis.name] = (axis_x,axis_y)
    elif(last_axis[axis.name] == (axis_x,axis_y)):
        return None
    last_axis[axis.name] = (axis_x,axis_y)
    return (axis_x,axis_y)

# for xbox control
def on_left_axis_moved(axis):
    axis = on_axis_moved(axis)
    if(axis):
        axis_x,axis_y = axis
        print(loco.get_motor_msg(axis_x,axis_y))
        scheduler.communicate(loco.get_motor_msg(axis_x,axis_y))

# for xbox controll
def on_right_axis_moved(axis):
    axis = on_axis_moved(axis)
    if(axis):
        axis_x,axis_y = axis
        precise.update_arm_msg(axis_x,axis_y)
        scheduler.communicate(precise.get_arm_msg())
    
axis_last = (0,0)
def hat_axis_moved(axis):
    global axis_last
    # STRONG ARM HAND SERVO CONTROL
    if((axis.x,axis.y) == axis_last ):
        return
    axis_last = axis.x,axis.y
    if (axis.y == 1) :
        scheduler.communicate(strong.move_hand(1))
    elif (axis.y == -1):
        scheduler.communicate(strong.move_hand(2))
    else:
        scheduler.communicate(strong.move_hand(3))

    # STRONG ARM SPIN SERVO CONTROL
    if (axis.x == 1) :
        scheduler.communicate(strong.move_spin(1))
    elif (axis.x == -1):
        scheduler.communicate(strong.move_spin(2))
    else:
        scheduler.communicate(strong.move_spin(3))    

# give function handlers to xbox controller package

def stop_all():
    """
    kill switch for the robot (might not work right)
    """
    #scheduler.communicate(precise.zero())
    #scheduler.communicate(strong.zero())
    scheduler.communicate(loco.zero())
    #scheduler.communicate(hR.zero())

def xboxcontroller_init():
    while(not Xbox360Controller.get_available()):
        print("Looking for Controller")
        time.sleep(.5)
    controller = Xbox360Controller(0)
    try:
        print("Controller Found")

        controller.button_b.when_pressed = lambda x: scheduler.communicate(strong.move_shoulder(2))
        controller.button_b.when_released = lambda x: scheduler.communicate(strong.move_shoulder(0))

        controller.button_a.when_pressed = lambda x: scheduler.communicate(strong.move_shoulder(1))
        controller.button_a.when_released = lambda x: scheduler.communicate(strong.move_shoulder(0))
    
        controller.button_select.when_pressed = lambda x: scheduler.communicate(hR.leftButton())
        controller.button_select.when_released = lambda x: scheduler.communicate(hR.zero())

        controller.button_y.when_released = lambda x: scheduler.communicate(precise.example_arm_msg())
        controller.button_x.when_pressed = lambda x: (stop_all())

        controller.button_start.when_pressed = lambda x: scheduler.communicate(hR.rightButton())
        controller.button_start.when_released = lambda x: scheduler.communicate(hR.zero())


        # Button trigger l (Left Bumper) events
        controller.button_trigger_l.when_pressed = lambda x: scheduler.communicate(strong.move_elbow(2))
        controller.button_trigger_l.when_released = lambda x: scheduler.communicate(strong.move_elbow(0))

        # Button trigger r (Right Bumper) events
        controller.button_trigger_r.when_pressed = lambda x: scheduler.communicate(strong.move_elbow(1))
        controller.button_trigger_r.when_released = lambda x: scheduler.communicate(strong.move_elbow(0))

        # Hat/DPAD movement event 
        controller.hat.when_moved = hat_axis_moved
        #controller.axis_l.when_moved = on_left_axis_moved
        controller.axis_r.when_moved = on_right_axis_moved

        controller.button_thumb_r.when_released = lambda x: scheduler.communicate(precise.get_arm_msg()) 

        controller.button_thumb_l.when_released = lambda x: playsound(r2d2sounds[random.randint(0,4)])

        
    except KeyboardInterrupt:
        pass
    except OSError:
        print("controller disconnected")
        # xboxcontroller.control()


def xboxcontroller_control(controller):
    print("Control")
    signal.pause()
  
    
def xboxcontroller():
    global scheduler 
    scheduler = client.Client("xboxcontroller")
    print("handshaking")
    scheduler.handshake()
    print("xbox thread started")
    xboxcontroller_init()
    last=False
    last_time = time.time()
    controller = Xbox360Controller()
    while(True):
        if ((abs(controller.axis_l.x) > .3) or (abs(controller.axis_l.y) > .3)):
            #print("Check")
            on_left_axis_moved(controller.axis_l)
            last=True
        elif last:
            scheduler.communicate(loco.zero())
            last = False
        #print(controller.axis_l.x, controller.axis_l.y)
        time.sleep(.05)
        # if KeyboardInterrupt:
        #     scheduler.close()
        #     break


if __name__ == "__main__":
    xboxcontroller()

      
# cat.close()
