import sys, time, random # Default Python Libraries
path: str = sys.argv[1]; sys.path.insert(0, path) # Modifying Python Path

from xbox360controller import Xbox360Controller # Xbox Controller
from playsound import playsound # Sound Player
from typing import Dict, List, Optional, Tuple # Typing

from scheduler.config import * # Configuration
from scheduler.client import Client # Client
from scheduler.utils import Message, printc # Utilities

from api.locomotionAPI import * # Locomotion Utilities
from api.preciseAPI import * # Precise Utilities
from api.strongAPI import * # Strong Utilities
from api.rotateAPI import * # Rotate Utilities

last_axis: Dict[str, Tuple] = {}
strong_axis: Tuple          = (0, 0)
threshold: float            = .5

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

    if (axis.name not in last_axis): last_axis[axis.name] = (axis_x, axis_y)
    elif (last_axis[axis.name] == (axis_x, axis_y)): return None

    last_axis[axis.name] = (axis_x, axis_y)
    return (axis_x, axis_y)

def on_left_axis_moved(axis: any) -> None:
    """
    Handles the movement of the left axis and sends the data to the scheduler.

    @param axis: Axis values of the controller.
    """
    axis_values: Optional[tuple[float, float]] = on_axis_moved(axis)
    if (axis_values is not None):
        axis_x, axis_y = axis_values
        client.communicate('put', get_locomotion(axis_x, axis_y))

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

    # STRONG ARM HAND SERVO CONTROL
    if (axis.y == 1):    client.communicate('put', move_hand(1))
    elif (axis.y == -1): client.communicate('put', move_hand(2))
    else:                client.communicate('put', move_hand(3))

    # STRONG ARM SPIN SERVO CONTROL
    if (axis.x == 1):    client.communicate('put', move_spin(1))
    elif (axis.x == -1): client.communicate('put', move_spin(2))
    else:                client.communicate('put', move_spin(3))

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
        controller.button_b.when_pressed  = lambda _: client.communicate('put', move_shoulder(2))
        controller.button_b.when_released = lambda _: client.communicate('put', move_shoulder(0))

        controller.button_a.when_pressed  = lambda _: client.communicate('put', move_shoulder(1))
        controller.button_a.when_released = lambda _: client.communicate('put', move_shoulder(0))

        controller.button_select.when_pressed  = lambda _: client.communicate('put', left_rotate())
        controller.button_select.when_released = lambda _: client.communicate('put', zero_rotate())

        controller.button_y.when_released = lambda _: client.communicate('put', example_precise())
        controller.button_x.when_pressed  = lambda _: stop_all()

        controller.button_start.when_pressed  = lambda _: client.communicate('put', right_rotate())
        controller.button_start.when_released = lambda _: client.communicate('put', zero_rotate())

        # Button trigger L (Left Bumper) events
        controller.button_trigger_l.when_pressed  = lambda _: client.communicate('put', move_elbow(2))
        controller.button_trigger_l.when_released = lambda _: client.communicate('put', move_elbow(0))

        # Button trigger R (Right Bumper) events
        controller.button_trigger_r.when_pressed  = lambda _: client.communicate('put', move_elbow(1))
        controller.button_trigger_r.when_released = lambda _: client.communicate('put', move_elbow(0))

        # Hat/DPAD movement event
        controller.hat.when_moved    = hat_axis_moved
        # controller.axis_l.when_moved = on_left_axis_moved
        controller.axis_r.when_moved = on_right_axis_moved

        controller.button_thumb_r.when_released = lambda _: client.communicate('put', get_precise())
        controller.button_thumb_l.when_released = lambda _: playsound(sounds[random.randint(0, 4)])

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

    while True:
        if ((abs(controller.axis_l.x) > .3) or (abs(controller.axis_l.y) > .3)):
            on_left_axis_moved(controller.axis_l)
            last = True
        elif last:
            client.communicate('put', zero_locomotion())
            last = False
        time.sleep(.05)
