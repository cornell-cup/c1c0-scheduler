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
    
    
# test
def testbutton(button):
	print('it works')

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
			
			''''
			# Left and right triggers move event
			controller.button_thumb_l.when_pressed = on_button_pressed
			controller.button_thumb_l.when_released = on_button_released
			controller.button_thumb_r.when_pressed = on_button_pressed
			controller.button_thumb_r.when_released = on_button_released

			# test
			controller.trigger_l.when_moved = testbutton
			controller.trigger_r.when_moved = testbutton
			
			Notes: 
			button_thumb_l corresponds to the the Right Trigger
			it prints when pressed and released
			but it also prints 'axis_r moved to 0 {-1, 0, or 1}'
				this seems like a bug, since axis_r should be the Right Joystick
			
			button_thumb_r does NOT correspond to the Left Trigger
			movement of the Left Trigger prints axis_r movement as well, but it differs from the Right Trigger
				????????
			
			button_x does not work
			'''
			
			# Bumper buttons
			controller.button_select.when_pressed = on_button_pressed
			controller.button_select.when_released = on_button_released
			controller.button_mode.when_pressed = on_button_pressed
			controller.button_mode.when_released = on_button_released
			
			# Button X and B events
			controller.button_x.when_pressed = on_button_pressed
			controller.button_x.when_released = on_button_released
			controller.button_b.when_pressed = on_button_pressed
			controller.button_b.when_released = on_button_released

			signal.pause()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	while True:
		xboxcontroller()
		time.sleep(0.2)
		if KeyboardInterrupt:
			break
