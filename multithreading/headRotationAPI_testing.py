import HeadRotation_XBox_API as hR
import time

i = 0
hR.open()
try:
	while(True):
		i = i+1
		if i % 10 == 0:
			hR.zero()
		elif i%5 == 0:
			hR.leftButton()
		else:
			hR.rightButton()
		#time.sleep(0.2)
except:
	hR.close()
