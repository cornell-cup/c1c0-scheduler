# To be called in multiserver when communicating with the XBox Controller. Calls leftButton or rightButton based on what was pushed

import HeadRotation_XBox_API as hR
import R2Protocol2 as r2p

open = 0

def buttonCall(eButton):
	global open
	if not open:
		hR.open()
		open = 1
	data = r2p.decode(eButton)
	msg = data[1]
	if 'button_trigger_l' in msg and ('held' in msg or 'pressed' in msg):
		hR.leftButton()
	elif 'button_trigger_r' in msg and ('held' in msg or 'pressed' in msg):
		hR.rightButton()
	elif ('button_trigger_l' in msg or 'button_trigger_r' in msg) and 'released' in msg:
		hR.close()
		open = 0

