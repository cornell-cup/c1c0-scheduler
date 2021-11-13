from xbox360controller import Xbox360Controller
import signal
import time

# for xbox control: kill all thread except chatbot
def on_button_pressed(button):    
    print('Button {0} was pressed'.format(button.name))

# for xbox control
def on_button_released(button):
    print('Button {0} was released'.format(button.name))

# for xbox control
def on_axis_moved(axis):
    # TODO send command to locomotion to control the head rotatioon
    # print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    if(axis.x <= -0.5):
        axis_x = -1
    elif(axis.x <= 0.5):
        axis_x = 0
    else:
        axis_x = 1
    if(axis.y <= -0.5):
        axis_y = -1
    elif(axis.y <= 0.5):
        axis_y = 0
    else:
        axis_y = 1
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis_x, axis_y))

# give function handlers to xbox controller package
def xboxcontroller():
	try:
		with Xbox360Controller(0, axis_threshold=0.2) as controller:
			# Button A events
			controller.button_a.when_pressed = on_button_pressed
			controller.button_a.when_released = on_button_released

			# Left and right axis move event
			controller.axis_l.when_moved = on_axis_moved
			controller.axis_r.when_moved = on_axis_moved

			signal.pause()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	while True:
		xboxcontroller()
		time.sleep(0.2)
		if KeyboardInterrupt:
			break
