import sys, time, random # Default Python Libraries
path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path

from xbox360controller import Xbox360Controller # Xbox Controller
from playsound import playsound # Sound Player
from typing import Dict, List, Optional, Tuple # Typing

from scheduler.config import * # Configuration
from scheduler.client import Client # Client
from scheduler.utils import Message, printc # Utilities
from api.carrAPI import trigger_carriage # for carriage
from api.locomotionAPI import * # Locomotion Utilities
from api.preciseAPI import * # Precise Utilities
from api.strongAPI import * # Strong Utilities
from api.rotateAPI import * # Rotate Utilities

last_axis: Dict[str, Tuple] = {}
strong_axis: Tuple          = (0, 0)
threshold: float            = .5
d_toggle = True #true is loco false is strong arm

def change_d_toggle():
    global d_toggle
    d_toggle = not d_toggle
    print(d_toggle)

def left_trigger_move(val: float):
    if (val == 0.0): client.communicate('put', move_shoulder(0))
    elif (val > 0.5): client.communicate('put', move_shoulder(1))

def right_trigger_move(val: float):
    if (val == 0.0): client.communicate('put', move_shoulder(0))
    elif (val > 0.5): client.communicate('put', move_shoulder(2))

def on_axis_moved(axis: any) -> Optional[Tuple[float, float]]:
    """
    Converts controller values of an axis to a tuple of floats depending on a threshold.

    @param axis: Axis values of the controller.
    @return: Tuple of floats or None.
    """

    global last_axis, threshold
    time.sleep(0.01)

    if (axis.x <= -threshold):  axis_x = -1
    elif (axis.x >= threshold): axis_x = 1
    else:                       axis_x = 0

    if (axis.y <= -threshold):  axis_y = 1
    elif (axis.y >= threshold): axis_y = -1
    else:                       axis_y = 0
    print(f'x axis {axis.x}')
    print(f'y axis {axis.y}')
    # if (axis.name not in last_axis): last_axis[axis.name] = (axis_x, axis_y)
    # elif (last_axis[axis.name] == (axis_x, axis_y)): return None

    last_axis[axis.name] = (axis_x, axis_y)
    return (axis_x, axis_y)

# def on_left_axis_moved(axis: any) -> None:
#     """
#     Handles the movement of the left axis and sends the data to the scheduler.

#     @param axis: Axis values of the controller.
#     """
#     axis_values: Optional[tuple[float, float]] = on_axis_moved(axis)
#     print(axis_values)
#     #if (axis_values is not None):
#         # axis_x, axis_y = axis_values
#         # client.communicate('put', get_locomotion(axis_x, axis_y))

def on_right_axis_moved(axis: any) -> None:
    """
    Handles the movement of the right axis and sends the data to the scheduler.

    @param axis: Axis values of the controller.
    """

    axis_values: Optional[Tuple[float, float]] = on_axis_moved(axis)
    if (axis_values is not None):
        axis_x, axis_y = axis_values
        update_precise(axis_x, axis_y)
        client.communicate('put', get_precise())

def hat_axis_moved(axis):
    """
    Handles the movement of the hat axis and sends the data to the scheduler.

    @param axis: Axis values of the controller.
    """
    global strong_axis

    if ((axis.x, axis.y) == strong_axis): return
    strong_axis = (axis.x, axis.y)

    if (d_toggle):
        loco_xy = [0,0]
        # loco control ---> forward and backward
        if (axis.y == 1):    loco_xy[1] = 1
        elif (axis.y == -1): loco_xy[1] = -1
        else:                loco_xy[1] = 0

        # loco control ---> spin turn left, spin turn right
        if (axis.x == 1):    loco_xy[0] = 1
        elif (axis.x == -1):  loco_xy[0] = -1
        else:                 loco_xy[0] = 0

        client.communicate('put', get_locomotion(loco_xy[0], loco_xy[1]))

    else:
        # STRONG ARM HAND SERVO CONTROL
        if (axis.y == 1):    client.communicate('put', move_hand(1))
        elif (axis.y == -1): client.communicate('put', move_hand(2))
        else:                client.communicate('put', move_hand(3))

        # STRONG ARM SPIN SERVO CONTROL
        if (axis.x == 1):    client.communicate('put', move_spin(1))
        elif (axis.x == -1): client.communicate('put', move_spin(2))
        else:                client.communicate('put', move_spin(3))

#def left_axis_moved(axis):


def stop_all() -> None:
    """
    Kill switch for the robot (might not work right)
    """

    client.communicate('put', zero_locomotion())
    # client.communicate('put', zero_precise())
    # client.communicate('put', zero_strong())

def xboxcontroller_init() -> None:
    """
    Initializes the Xbox Controller and sets up the event handlers.
    """

    while (not Xbox360Controller.get_available()):
        print("Looking For Controller")
        time.sleep(1)

    controller: Xbox360Controller = Xbox360Controller(0)
    print("Controller Connected")

    try:
        # Button Trigger L (Left Bumper) events
        controller.button_trigger_l.when_pressed  = lambda _: client.communicate('put', move_elbow(1))
        controller.button_trigger_l.when_released = lambda _: client.communicate('put', move_elbow(0))

        # Button Trigger R (Right Bumper) events
        controller.button_trigger_r.when_pressed  = lambda _: client.communicate('put', move_elbow(2))
        controller.button_trigger_r.when_released = lambda _: client.communicate('put', move_elbow(0))

        # Trigger R and L events
        controller.trigger_l.when_moved = lambda _: left_trigger_move(controller.trigger_l.value)
        controller.trigger_r.when_moved = lambda _: right_trigger_move(controller.trigger_r.value)

        # Select and start events
        controller.button_select.when_pressed  = lambda _: client.communicate('put', left_rotate())
        controller.button_select.when_released = lambda _: client.communicate('put', zero_rotate())

        #carriage
        controller.button_b.when_pressed  = lambda _: client.communicate('put', trigger_carriage())
        #

        controller.button_start.when_pressed  = lambda _: client.communicate('put', right_rotate())
        controller.button_start.when_released = lambda _: client.communicate('put', zero_rotate())

        controller.button_y.when_released = lambda _: client.communicate('put', example_precise())
        controller.button_x.when_pressed  = lambda _: change_d_toggle()

        # Hat/DPAD movement event
        controller.hat.when_moved    = hat_axis_moved
        controller.axis_r.when_moved = on_right_axis_moved

        # controller.button_thumb_r.when_released = lambda _: client.communicate('put', get_precise())
        controller.button_a.when_pressed = lambda _: playsound(sounds[random.randint(0, 4)])


        #controller.axis_l.when_moved = lambda _: on_left_axis_moved(controller.axis_l) #print(controller.axis_l.y)

    except KeyboardInterrupt: pass
    except OSError: print("Controller Disconnected")

if __name__ == '__main__':
    # Initializing client
    client: Client = Client('xbox')
    client.connect()

    # Obtaining R2D2 sounds
    sounds: List[str] = []
    for i in range(1, 6): sounds.append('../assets/r2d2-'+str(i)+'.mp3')

    # Initializing Xbox Controller
    xboxcontroller_init()
    last, last_time = False, time.time()
    controller = Xbox360Controller()

    # while True:
    #     time.sleep(.25)

    #     if ((abs(controller.axis_l.x) > .3) or (abs(controller.axis_l.y) > .3)):
    #         on_left_axis_moved(controller.axis_l)
    #         last = True
    #     elif last:
    #         client.communicate('put', zero_locomotion())
    #         print('zeroed')
    #         last = False
    #     time.sleep(.02)

        # print(controller.trigger_r.value)
        # print(controller.trigger_l.value)
