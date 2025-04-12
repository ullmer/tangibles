# IMU json listener
# Brygg Ullmer and Brandon Spears, Clemson University
# Begun 2025-04-11 

import sys
import json

#https://learn.adafruit.com/adafruit-lsm6ds3tr-c-6-dof-accel-gyro-imu/python-circuitpython
#https://github.com/xioTechnologies/Fusion/blob/main/Python/simple_example.py

try:    import imufusion
except: print("imufusion class not found!"); sys.exit(-1)


class enoIMUjlistener: #enodia IMU JSON ~listener

  #accelGyroJsonFmt = "{s:ag1, a:[%2.2f,%2.2f,%2.2f], g:[%2.2f,%2.2f,%2.2f]}" 
  lastUpdateInTicks = -1
  currentPos        = None
  currentOrient     = None
  ahrs              = None

  ######### constructor #########

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.initImuFsn()

  def initImuFsn(self): self.ahrs = imufusion.Ahrs()

  def msg(self, msgStr): print("enoIMUjlistener: " + str(msgStr)) #toward future redirectability

  ######### parse accelerometer/gyro json #########

  def parseAccelGyroJson(self, agStr):
    try:
      parsed_data = json.loads(agStr)

      self.feedAhrsAccelGyroJson(self, agDict)

  ######### parse accelerometer/gyro json #########

  def feedAhrsGyroJson(self, agDict):

    if 's' not in agDict:    self.msg("feedAhrsGyroJson: sensor spec not present");  return False
    if agDict['s'] != 'ag1': self.msg("feedAhrsGyroJson: sensor ag1 not indicated"); return False


    return result

### end ###
