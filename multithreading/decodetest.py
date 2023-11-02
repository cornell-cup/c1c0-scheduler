import serial
import sys
import time

sys.path.append('../../c1c0-movement/c1c0-movement/Locomotion')
import R2Protocol2
import locomotion_API

ser = serial.Serial(
  port = '/dev/ttyTHS1',
  baudrate = 115200,
)

def writeToSerial(writeArray):
  '''
  This functions writes a byte array from the Jetson to the Locomotion Arduino using R2Protocol. 
  
  The input 'writeArray' is length 13.
  
  For example, to get Joints 2 and 3 to move to angles 80 and 90. 
  Say the previous writetoSerial command was [10,20,30,40,50,60]. 
  The next command would then be: writeToSerial([10,80,90,40,50,60]).
  So, change the indices you want to change, and keep the previous
  angles for the joints you don't want to move.
  '''
  # LOCO = Locomotion
  # cast writeArray from int to byte, encode the array using the R2Protocol
  write_byte = R2Protocol2.encode(bytes('LOCO','utf-8'), bytearray(writeArray))
  
  #data = "(+1.23,-4.56)"
  
  locomotion_API.locomotion_msg(writeArray) # serial port: /dev/ttyTHS1 USB port: /dev/ttyACM0
  print("message sent: " + writeArray)
  
  
  
  
  
  # send the encoded array across the Jetson Serial lines
  #ser.write(write_byte)
  
  
# For Debugging Purposes  
# arm should move from start position to 60 to 100 to 20 then stop
data = "(+1.23,-4.56)"
  
locomotion_API.locomotion_msg(data)
print("message sent: " + data)
'''
array1 = (+1.23,-4.56)
array2 = (+1.00,-1.00)
array3 = (-1.00,+1.00)

writeToSerial(array1)
print("first send: ", array1)
time.sleep(5)
writeToSerial(array2)
print("second send:", array2)
time.sleep(5)
writeToSerial(array3)
print("third send: ", array3)
'''

