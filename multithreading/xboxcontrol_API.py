from xbox360controller import Xbox360Controller
import signal
import time
import client
import HeadRotation_XBox_API as hR
import Locomotion_API as loco
import strongarm_API as strong
import arm_API as precise



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
    if(axis.x <= -0.8):
        axis_x = -1
    elif(axis.x >= .8):
        axis_x = 1
    else:
        axis_x = 0
    if(axis.y <= -0.8):
        axis_y = 1
    elif(axis.y >= .8):
        axis_y = -1
    else:
        axis_y = 0
    if(axis.name not in last_axis):
        last_axis[axis.name] = (axis_x,axis_y)
    elif(last_axis[axis.name] == (axis_x,axis_y)):
        return
    last_axis[axis.name] = (axis_x,axis_y)
    return (axis_x,axis_y)

# for xbox control
def on_left_axis_moved(axis):
    axis = on_axis_moved(axis)
    if(axis):
        axis_x,axis_y = axis
        scheduler.communicate(loco.get_motor_msg(axis_x,axis_y))

# for xbox controll
def on_right_axis_moved(axis):
    axis = on_axis_moved(axis)
    if(axis):
        axis_x,axis_y = axis
        precise.update_arm_msg(axis_x,axis_y)
    
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
def xboxcontroller_control():
  
  try:
    while(not Xbox360Controller.get_available()):
        print("Looking for Controller")
        time.sleep(.5)
    print("Controller Found")
    with Xbox360Controller(0, axis_threshold=0.5) as controller:

        controller.button_b.when_pressed = lambda x: scheduler.communicate(strong.move_shoulder(2))
        controller.button_b.when_released = lambda x: scheduler.communicate(strong.move_shoulder(0))

        controller.button_a.when_pressed = lambda x: scheduler.communicate(strong.move_shoulder(1))
        controller.button_a.when_released = lambda x: scheduler.communicate(strong.move_shoulder(0))
        
        controller.button_select.when_pressed = lambda x: scheduler.communicate(hR.leftButton())
        controller.button_select.when_released = lambda x: scheduler.communicate(hR.zero())

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
        controller.axis_l.when_moved = on_left_axis_moved
        controller.axis_r.when_moved = on_right_axis_moved

        controller.button_x.when_released = lambda x: scheduler.communicate(precise.get_arm_msg()) 

        while True:
            continue
        signal.pause()
      
  except KeyboardInterrupt:
    pass

def xboxcontroller():
    global scheduler 
    scheduler = client.Client("xboxcontroller")
    scheduler.handshake()
    while True:
        xboxcontroller_control()
        time.sleep(0.2)
        if KeyboardInterrupt:
            scheduler.close()
            break


if __name__ == "__main__":
    scheduler = client.Client("xboxcontroller")
    scheduler.handshake()

    while True:
        xboxcontroller_control()
        time.sleep(0.2)
        if KeyboardInterrupt:
            scheduler.close()
            break
      
# cat.close()
