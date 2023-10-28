from xbox360controller import Xbox360Controller
import signal
import time
import client
import HeadRotation_XBox_API as hR
import strongarm_API as strong


motor_angles = [0,0,0,0,0,0]
motor_index = 0
# for xbox control: kill all thread except chatbot
def on_button_pressed(button):   
    global motor_angles
    if(button.name == 'button_a'):
        #scheduler.communicate('xbox: (+0.00,+0.00)')
        scheduler.communicate(strong.move_shoulder(1))
    if(button.name == 'button_b'):
        #scheduler.communicate('xbox: (+0.00,+0.00)')
        scheduler.communicate(strong.move_shoulder(2))
    if(button.name == 'button_thumb_r'):
        scheduler.communicate("precise: " + str(motor_angles))


# for xbox control
def on_button_released(button):
    # STRONG ARM ELBOW CONTROL
    if(button.name == 'button_trigger_l'):
        scheduler.communicate(strong.move_elbow(0))
    elif(button.name == 'button_trigger_r'):
        scheduler.communicate(strong.move_elbow(0))
    
    # STRONG ARM SHOUDLER CONTROL
    if(button.name == 'button_a' or button.name == 'button_b'):
        scheduler.communicate(strong.move_shoulder(3))
# for xbox control
def on_button_held(button):
    #print('Button {0} was released'.format(button.name))
    #print(button.name)
    #scheduler.communicate('xbox: ' + str(button.name) + ' held')
    #scheduler.communicate('Xbox:(MNOPQR)')
    #scheduler.communicate('xbox: (+1.00,-1.00)')
    #str1 = 'Xbox: '+str(button.name)+' held'
    #scheduler.communicate(str(button.name))
    #return button.name
    
    # STRONG ARM ELBOW CONTROL
    if(button.name == 'button_trigger_l'):
        scheduler.communicate(strong.move_elbow(2))
        #scheduler.communicate(hR.leftButton())
        #hR.leftButton()
        #scheduler.communicate('xbox: (-2.00,-2.00)')
    elif(button.name == 'button_trigger_r'):
        scheduler.communicate(strong.move_elbow(1))
        #scheduler.communicate(hR.rightButton())
        #scheduler.communicate('xbox: (+2.00,+2.00)')
        #hR.rightButton()

    # LOCOMOTION
    if(button.name == 'button_x'):
        scheduler.communicate('xbox: (+0.00,+0.00)')
    if(button.name == 'button_y'):
        #scheduler.communicate('xbox: (+0.00,+0.00)')
        scheduler.communicate(hR.zero())

    if(button.name == 'button_a'):
        scheduler.communicate(strong.move_shoulder(1))
    if(button.name == 'button_b'):
        #scheduler.communicate('xbox: (+0.00,+0.00)')
        scheduler.communicate(strong.move_shoulder(2))

# for xbox control
def on_axis_moved(axis):
    # TODO send command to locomotion to control the head rotatioon
    # print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    if(axis.x <= -0.8):
        axis_x = -1
    elif(axis.x <= 0.8):
        axis_x = 0
    else:
        axis_x = 1
    if(axis.y <= -0.8):
        axis_y = 1
    elif(axis.y <= 0.8):
        axis_y = 0
    else:
        axis_y = -1
    lvalue = 0
    rvalue = 0
    if(axis_x == 0 and axis_y == 1):
        lvalue = '+' + str(0.2) + '0'
        rvalue = '+' + str(0.2) + '0'
    elif(axis_x == 0 and axis_y == -1):
        lvalue = '-' + str(0.2) + '0'
        rvalue = '-' + str(0.2) + '0'
    elif(axis_x == -1 and axis_y == 0):
        lvalue = '-' + str(0.2) + '0'
        rvalue = '+' + str(0.2) + '0' 
    elif(axis_x == 1 and axis_y == 0):
        lvalue = '+' + str(0.2) + '0'
        rvalue = '-' + str(0.2) + '0'
    scheduler.communicate('xbox: (' + str(lvalue) + ',' + str(rvalue) + ')')

# for xbox control
def on_r_axis_moved(axis):
    global motor_angles
    global motor_index
    # TODO send command to locomotion to control the head rotatioon
    # print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    if(axis.x <= -0.8):
        axis_x = -1
    elif(axis.x <= 0.8):
        axis_x = 0
    else:
        axis_x = 1
    if(axis.y <= -0.8):
        axis_y = 1
    elif(axis.y <= 0.8):
        axis_y = 0
    else:
        axis_y = -1
    lvalue = 0
    rvalue = 0
    if(axis_x == 0 and axis_y == 1):
        if(motor_index == 0):
            motor_angles[motor_index] += 3
        elif(motor_index == 2):
            motor_angles[motor_index] += 5
            if motor_angles[motor_index] < 0:
                motor_angles[motor_index] = 0
        else:
            motor_angles[motor_index] += 5
            if motor_angles[motor_index] < 0:
                motor_angles[motor_index] = 0
        print(motor_angles)
    elif(axis_x == 0 and axis_y == -1):
        if(motor_index == 0):
            motor_angles[motor_index] -= 3
        elif(motor_index == 2):
            motor_angles[motor_index] -= 5
        else:
            motor_angles[motor_index] -= 5
        print(motor_angles)
    elif(axis_x == -1 and axis_y == 0):
        motor_index -= 1
        if(motor_index == -1):
            motor_index = 5
        print(motor_index)
    elif(axis_x == 1 and axis_y == 0):
        motor_index += 1
        if(motor_index == 6):
            motor_index = 0
        print(motor_index)

def nonzero_axis(axis):
    if(axis.x <= -0.8):
        axis_x = -1
    elif(axis.x <= 0.8):
        axis_x = 0
    else:
        axis_x = 1
    if(axis.y <= -0.8):
        axis_y = 1
    elif(axis.y <= 0.8):
        axis_y = 0
    else:
        axis_y = -1
        
    if axis_x == 1 or axis_x == -1 or axis_y == 1 or axis_y == -1:
        #print("value is: " + str(axis.x) + "  " + str(axis.y))
        #print("convert into: " + str(axis_x) + "  " + str(axis_y))
        return True
    return False

    #return [str(axis_x), str(axis_y)]
    # (+0.00,-0.00)

axis_last = None
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

    
 #test
#def testbutton(button

# for communication to xboxToLoco.py
# cat = open('xboxToLoco.py')


# give function handlers to xbox controller package
def xboxcontroller_control():
  
  try:
    while(not Xbox360Controller.get_available()):
        print("Looking for Controller")
        time.sleep(.5)
    print("Controller Found")
    with Xbox360Controller(0, axis_threshold=0.5) as controller:
        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        controller.button_a.when_released = on_button_released

        # Left and right axis move event
        #controller.axis_l.when_moved = on_axis_moved
        #controller.axis_r.when_moved = on_axis_moved
        
        # Button B events
        controller.button_b.when_pressed = on_button_pressed
        controller.button_b.when_released = on_button_released

        controller.button_select.when_pressed = lambda x: scheduler.communicate(hR.leftButton())
        controller.button_select.when_released = lambda x: scheduler.communicate(hR.zero())

        controller.button_start.when_pressed = lambda x: scheduler.communicate(hR.rightButton())
        controller.button_start.when_released = lambda x: scheduler.communicate(hR.zero())
        
        # Button X events
        controller.button_x.when_pressed = on_button_pressed
        controller.button_x.when_released = on_button_released

        # Button trigger l (Left Bumper) events
        controller.button_trigger_l.when_pressed = on_button_pressed
        controller.button_trigger_l.when_released = on_button_released

        # Button trigger r (Right Bumper) events
        controller.button_trigger_r.when_pressed = on_button_pressed
        controller.button_trigger_r.when_released = on_button_released

        # Hat/DPAD movement event 
        controller.hat.when_moved = hat_axis_moved

        controller.button_thumb_r.when_pressed = on_button_pressed
        controller.button_thumb_r.when_released = on_button_released

        while True:
            #if controller.button_a.is_pressed: # is_pressed is a boolean
            # on_button_held(controller.button_a)
            # time.sleep(0.2)
            if controller.button_trigger_l.is_pressed: # is_pressed is a boolean
                on_button_held(controller.button_trigger_l)
                time.sleep(0.2)
            if controller.button_trigger_r.is_pressed: # is_pressed is a boolean
                on_button_held(controller.button_trigger_r)
                time.sleep(0.2)
            if controller.button_x.is_pressed:
                on_button_held(controller.button_x)
            if controller.button_y.is_pressed:
                on_button_held(controller.button_y)
            if nonzero_axis(controller.axis_l):
                on_axis_moved(controller.axis_l)
                time.sleep(0.2)
            if nonzero_axis(controller.axis_r):
                on_r_axis_moved(controller.axis_r)
                time.sleep(0.2)


            #TODO add axis value polling
            
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
    #try:
    #except:
    #   print("Scheduler handshake unsuccesful")
    while True:
        xboxcontroller_control()
        time.sleep(0.2)
        if KeyboardInterrupt:
            scheduler.close()
            break
      
# cat.close()
