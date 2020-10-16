import serial
import time

ser_precise = 0
wave_commands = ["M2D90E", "M3D60E", "M5D90E", "M3D90E", "M3D30E", "M3D90E", "M3D30E", "M3D90E", "M3D30E", "M0D0E"]
grab_commands = ["M1D90E", "M2D90E", "M3D60E", "M5D-90E", "M6D45E", "M6D0E", "M0D0E"]

def open_ser_precise():
    ser_precise = serial.Serial('/dev/precisearm', 9600)
    
def reset_precise():
    ser_precise.write("M0D0E".encode('utf-8'))
    ser_precise.close()
    
def wave():
    for command in wave_commands:
        ser_precise.write(command.encode('utf-8')
    ser_precise.close()
                          
def grab():
    for i in range(0,len(grab_commands)):
        if i == 5:
            time.sleep(0.5)
        ser_precise.write(command.encode('utf-8')
        i = i +1
    ser_precise.close()

