# IMU json listener
# Brygg Ullmer and Brandon Spears, Clemson University
# Begun 2025-04-11 

import sys

#https://learn.adafruit.com/adafruit-lsm6ds3tr-c-6-dof-accel-gyro-imu/python-circuitpython
#https://github.com/xioTechnologies/Fusion/blob/main/Python/simple_example.py

try:    import imufusion
except: print("imufusion class not found!"); sys.exit(-1)

class enoIMUjlistener: #enodia IMU JSON ~listener

  #accelGyroJsonFmt = "{s:ag1, a:[%2.2f,%2.2f,%2.2f], g:[%2.2f,%2.2f,%2.2f]}" 

  lastUpdateInTicks = -1

  def __init__(self): 

  def parseAccelGyroJson(self, accelGyroAxisVals):
    result = self.accelGyroJsonFmt % accelGyroAxisVals
    return result

### end ###
