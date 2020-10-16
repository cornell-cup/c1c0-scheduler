#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:
$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar


PORT_NAME = '/dev/lidar1'


def run_lidar():
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    #outfile = open('lidarResults.txt', 'w')
    
    print('Recording measurments... Press Crl+C to stop.')
    length = 0
    for measurment in lidar.iter_measurments():
        i = 0
        for distance in measurment:
            if i == 2:
                angle = distance
                print("angle " + str(angle))
            if i == 3:
                distance = distance / 25.4
                print("distance " + str(distance))
                if distance != 0 and distance < 12 and (angle > 245 or angle < 110):
                    lidar.stop()
                    lidar.disconnect()
                    print("in return")
                    return False
            i = i + 1
        if length > 200:
            lidar.stop()
            lidar.disconnect()
            print("disconnected lidar")
            return True
        
        length = length + 1
    #outfile.close()
