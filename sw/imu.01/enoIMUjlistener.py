# IMU json listener
# Brygg Ullmer, Clemson University
# Begun 2025-04-11 

import sys, json, traceback, time

#https://learn.adafruit.com/adafruit-lsm6ds3tr-c-6-dof-accel-gyro-imu/python-circuitpython
#https://github.com/xioTechnologies/Fusion/blob/main/Python/simple_example.py

#https://github.com/RPi-Distro/RTIMULib
#https://github.com/PaulKemppi/gtsam_fusion
#https://github.com/niru-5/imusensor
#https://pypose.org/tutorials/imu/imu_integrator_tutorial.html
#https://github.com/chengwei0427/Lidar_IMU_Localization
#https://www.dfrobot.com/blog-1647.html

try:    import imufusion
except: print("imufusion class not found!"); sys.exit(-1)
  
######### Enodia IMU json listener & imufusion transformer #########

class enoIMUjlistener: #enodia IMU JSON ~listener

  #accelGyroJsonFmt = "{s:ag1, a:[%2.2f,%2.2f,%2.2f], g:[%2.2f,%2.2f,%2.2f]}" 
  lastUpdateInTicks = -1
  currentPos        = None
  currentOrient     = None
  ahrs              = None
  lastTimeMs        = None

  ######### constructor #########

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.initImuFsn()
    self.lastTimeMs = self.getTimeMs()

  def getTimeMs(self):  return time.time_ns() // 1_000_000

  def initImuFsn(self): self.ahrs = imufusion.Ahrs()

  def msg(self, msgStr): print("enoIMUjlistener: " + str(msgStr)) #toward future redirectability

  ######### parse accelerometer/gyro json #########

  def parseAccelGyroJson(self, agStr):
    try:
      parsed_data = json.loads(agStr)
      self.feedAhrsAccelGyroJson(self, agDict)
    except: self.msg("parseAccelGyroJson exception"); traceback.print_exc()

  ######### parse accelerometer/gyro json #########

  def feedAhrsGyroJson(self, agDict, timeDelta):

    try:
      if 's' not in agDict:    self.msg("feedAhrsGyroJson: sensor spec not present");  return False
      if agDict['s'] != 'ag1': self.msg("feedAhrsGyroJson: sensor ag1 not indicated"); return False
      if 'a' not in agDict:    self.msg("feedAhrsGyroJson: accel data not present");   return False
      if 'g' not in agDict:    self.msg("feedAhrsGyroJson: gyro data not present");    return False

      a, g = agDict['a'], agDict['g']
      newTime = self.getTimeMs()
      timeDiffMs = newTime - self.lastTimeMs
      timeDelta  = float(timeDiffMs) / 1000.

      self.ahrs.update_no_magnetometer(g, a, timeDelta)
      self.lastTimeMs = newTime

    except: self.msg("parseAccelGyroJson exception"); traceback.print_exc(); return False
    return True

### end ###
