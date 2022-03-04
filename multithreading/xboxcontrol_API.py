from xbox360controller import Xbox360Controller
import signal
import time
import client

# for xbox control: kill all thread except chatbot
def on_button_pressed(button):    
    #print('Button {0} was pressed'.format(button.name))
    #print(button.name)
    scheduler.communicate('xbox: ' + str(button.name) + ' pressed')
    #return button.name

# for xbox control
def on_button_released(button):
    #print('Button {0} was released'.format(button.name))
    #print(button.name)
    scheduler.communicate('xbox: ' + str(button.name) + ' released')
    #return button.name

# for xbox control
def on_button_held(button):
    #print('Button {0} was released'.format(button.name))
    #print(button.name)
    scheduler.communicate('xbox: ' + str(button.name) + ' held')
    #return button.name

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
    #print(str(axis_x), str(axis_y))
    scheduler.communicate('xbox: axis: ' + str(axis_x) + ' ' + str(axis_y))
    #return [str(axis_x), str(axis_y)]
    
    
 #test
#def testbutton(button

# for communication to xboxToLoco.py
# cat = open('xboxToLoco.py')


# give function handlers to xbox controller package
def xboxcontroller_control():
	
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


			while True:
				if controller.button_a.is_pressed: # is_pressed is a boolean
					on_button_held(controller.button_a)
					time.sleep(0.2)
				if controller.button_b.is_pressed: # is_pressed is a boolean
					on_button_held(controller.button_b)
					time.sleep(0.2)
				if controller.button_x.is_pressed: # is_pressed is a boolean
					on_button_held(controller.button_x)
					time.sleep(0.2)
				if controller.button_trigger_l.is_pressed: # is_pressed is a boolean
					on_button_held(controller.button_trigger_l)
					time.sleep(0.2)
				if controller.button_trigger_r.is_pressed: # is_pressed is a boolean
					on_button_held(controller.button_trigger_r)
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
    # 	print("Scheduler handshake unsuccesful")
    while True:
        xboxcontroller_control()
        time.sleep(0.2)
        if KeyboardInterrupt:
            scheduler.close()
            break
			
# cat.close()
