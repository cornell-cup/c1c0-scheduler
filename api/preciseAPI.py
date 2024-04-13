from scheduler.config import * # Configurations

from typing import List # Typing

motor_angles = [0,0,0,0,0,0,0]
motor_index  = 0
state        = 0

def update_precise(axis_x, axis_y) -> None:
    """
    Update the motor angles based on the joystick input.

    @param axis_x: The x-axis direction of the joystick.
    @param axis_y: The y-axis direction of the joystick.
    """

    global motor_angles, motor_index

    if (axis_x == 0 and axis_y == 1):
        if   (motor_index == 0): motor_angles[motor_index] += 3
        elif (motor_index == 2): motor_angles[motor_index] += 5
        elif (motor_index == 3): motor_angles[motor_index] += 15
        else:                    motor_angles[motor_index] += 5
    elif (axis_x == 0 and axis_y == -1):
        if   (motor_index == 0): motor_angles[motor_index] -= 3
        elif (motor_index == 2): motor_angles[motor_index] -= 5
        elif (motor_index == 3): motor_angles[motor_index] -= 15
        else:                    motor_angles[motor_index] -= 5
    elif (axis_x == -1 and axis_y == 0):
        motor_index = (motor_index - 1) % len(motor_angles)
    elif(axis_x == 1 and axis_y == 0):
        motor_index = (motor_index + 1) % len(motor_angles)

    for index, angle in enumerate(motor_angles):
        if(angle < 0):
            motor_angles[index] = 0
            print(motor_angles[index])

    print(motor_angles)
    print("motor J" + str(motor_index+1))

def get_precise() -> str:
    """
    Creates message with current motor angles to send to scheduler.

    @return: The message with current motor angles.
    """

    global motor_angles
    return precise_encode(motor_angles)

def example_precise() -> str:
    """
    Creates an example message with motor angles to send to scheduler.

    @return: The example message with motor angles.
    """
    global state, motor_angles
    state = (state + 1) % 4

    if (state == 0):   motor_angles = [30, 75, 40, 80, 30,  5, motor_angles[6]]
    elif (state == 1): motor_angles = [60, 65, 10, 60, 90, 30, motor_angles[6]]
    elif (state == 2): motor_angles = [20, 55, 80, 10, 10, 50, motor_angles[6]]
    else:              motor_angles = [30, 75, 0, 60, 30, 30, motor_angles[6]]

    return precise_encode(motor_angles)

def zero_precise() -> str:
    """
    Creates a message with all motor angles set to 0.

    @return: The message with all motor angles set to 0.
    """

    global motor_angles
    motor_angles = [0, 0, 0, 0, 0, 0, motor_angles[6]]
    return precise_encode(motor_angles)

def precise_encode(motor_angles: List[int]) -> str:
    """
    Encodes the given motor angles into a message to send to the scheduler.

    @param motor_angles: The motor angles to encode.
    @return: The message with the encoded motor angles.
    """

    return 'precise: ' + str(motor_angles)

def precise_decode(msg: str) -> List[int]:
    """
    Decodes the given message into motor angles.

    @param msg: The message to decode.
    @return: The motor angles decoded from the message.
    """

    arr: list[str] = msg.split('[')[1].split(']')[0].split(',')
    return [int(i.strip()) for i in arr]
