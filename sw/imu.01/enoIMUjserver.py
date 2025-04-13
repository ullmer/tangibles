# IMU service class
# Brygg Ullmer, Clemson University
# Begun 2025-04-11 

import sys

#https://learn.adafruit.com/adafruit-lsm6ds3tr-c-6-dof-accel-gyro-imu/python-circuitpython
#https://github.com/xioTechnologies/Fusion/blob/main/Python/simple_example.py
#https://docs.circuitpython.org/en/latest/shared-bindings/alarm/
#https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html

try:    from adafruit_lsm6ds.lsm6ds3 import LSM6DS3 as LSM6DS
except: print("adafruit_lsm6ds class not found!"); sys.exit(-1)

import time
import board
import busio
import supervisor
import alarm

class enoIMUjserver: #enodia IMU JSON ~server

  i2c        = None
  accel_gyro = None
  pinSCL     = board.GP7
  pinSDA     = board.GP6
  address    = 0x6b
  imuInitialized   = False
  accelGyroJsonFmt = '{"s":"ag1", "a":[%6.2f,%6.2f,%6.2f], "g":[%6.2f,%6.2f,%6.2f]}'

  minUpdateMS = 1000 #ms
  maxUpdateMS = 10   #ms
  lastUpdateInTicks = -1

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.initIMU()
    self.lastUpdateInTicks = supervisor.ticks_ms()

  def initIMU(self):
    if self.i2c is None: self.i2c = busio.I2C(self.pinSCL, self.pinSDA)
    self.accel_gyro = LSM6DS(self.i2c, address=self.address)
    self.imuInitialized = True

  def readAccelGyro(self):
    a = self.accel_gyro.acceleration
    g = self.accel_gyro.gyro
    result = a+g
    return result

  def genAccelGyroJson(self, accelGyroAxisVals):
    result = self.accelGyroJsonFmt % accelGyroAxisVals
    return result

  def genAccelGyroJson2(self):
    accelGyroAxisVals = self.readAccelGyro()
    result = self.accelGyroJsonFmt % accelGyroAxisVals
    return result

### end ###
