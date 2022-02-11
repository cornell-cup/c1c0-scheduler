from xbox360controller import Xbox360Controller
import signal
import time

# for xbox control: kill all thread except chatbot
def on_button_pressed(button):    
    #print('Button {0} was pressed'.format(button.name))
    print(button.name)
    return button.name

# for xbox control
def on_button_released(button):
    #print('Button {0} was released'.format(button.name))
    print(button.name)
    return button.name

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
    #print('Axis {0} moved to {1} {2}'.format(axis.name, axis_x, axis_y))
    print(str(axis_x), str(axis_y))
    return [str(axis_x), str(axis_y)]
    
    
 #test
#def testbutton(button

# for communication to xboxToLoco.py
cat = open('xboxToLoco.py')


# give function handlers to xbox controller package
def xboxcontroller():
	try:
		with Xbox360Controller(0, axis_threshold=0.2) as controller:
			# Button A events
			controller.button_a.when_pressed = on_button_pressed
			controller.button_a.when_released = on_button_released

			# Left and right axis move event
			controller.axis_l.when_moved = on_axis_moved
			#controller.axis_r.when_moved = on_axis_moved
			
			# Left bumper button (small front button)
			controller.button_trigger_l.when_pressed = on_button_pressed
			controller.button_trigger_l.when_released = on_button_released
			
			# Right bumper button (small front button)
			controller.button_trigger_r.when_pressed = on_button_pressed
			controller.button_trigger_r.when_released = on_button_released
			
			# Button B events
			controller.button_b.when_pressed = on_button_pressed
			controller.button_b.when_released = on_button_released
			
			# Button X events
			controller.button_x.when_pressed = on_button_pressed
			controller.button_x.when_released = on_button_released
			
			'''
			Next Steps:
			use return instead of print, for axis return an array of axis_x, axis_y
			since there's only one axis used no need for axis name
			'''
			
			

			signal.pause()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	while True:
		xboxcontroller()
		time.sleep(0.2)
		if KeyboardInterrupt:
			break
			
cat.close()
