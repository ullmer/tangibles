# Enodia embedded devices json ~server 
# Brygg Ullmer, Clemson University
# Begun 2025-04-11 

import sys

#https://docs.circuitpython.org/en/latest/shared-bindings/alarm/
#https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html

import time
import alarm
import board
import busio
import digitalio
import traceback
import supervisor

from enoIMUjserver import *

class enoEmbedJserver: 

  i2c        = None
  pinSCL     = board.GP7
  pinSDA     = board.GP6
  address    = 0x6b
  verbose    = True

  minUpdateMs        =  1000  #ms
  maxUpdateMs        =  10    #ms
  scanLockPendingNap =  0.001 #s
  lastBroadcastMs    = -1
  onboardLED         = None
  onboardLEDPin      = board.GP25
  onboardLEDCycleDurSlow = 2.  #duration, in s
  onboardLEDCycleDurFast = 0.5 #duration, in s

  addressToDeviceDict = None

  imu     = None
  msAlarm = None

  def __init__(self): 
    self.lastBroadcastMs     = supervisor.ticks_ms()
    self.addressToDeviceDict = {}
    self.initI2C()
    self.initLED()
    self.initAlarm()

  def initLED(self):   
    self.onboardLED = digitalio.DigitalInOut(self.onboardLEDPin)
    self.onboardLED.direction = digitalio.Direction.OUTPUT
    self.onboardLED.value = True

  def msg(self, msgStr):   print("enoEmbedJserver msg: " + str(msgStr))
 
  def setLED(self, value): self.onboardLED.value = value  

  def initI2C(self):    self.i2c = busio.I2C(self.pinSCL, self.pinSDA)

  def initAlarm(self):  pass

  def nap(self):        self.msAlarm.light_sleep_until_alarm()

  def getTicksMs(self): return supervisor.ticks_ms()

  def setAlarm(self, duration): self.msAlarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + duration)

  def activateIMU(self): 
    try:
      self.imu = enoIMUjserver(i2c=self.i2c)
    except Exception as e:
      self.msg("activateIMU error")
      traceback.print_exception(e)
  
  def readIMU(self): return self.imu.genAccelGyroJson2()

  def ledCycle(self, duration): #initially, synchronous
    while True:
      self.setLED(True);  time.sleep(duration) #self.msAlarm.light_sleep
      self.setLED(False); time.sleep(duration) #self.msAlarm.light_sleep

  def ledCycleSlow(self): #initially, synchronous: 
    duration = self.onboardLEDCycleDurSlow
    self.ledCycle(duration)

  def ledCycleFast(self): #initially, synchronous: 
    duration = self.onboardLEDCycleDurFast
    self.ledCycle(duration)

  def msSinceLastBroadcast(self): 
    if self.lastBroadcastMs < 0: return self.lastBroadcastMs
    return self.getTicksMs() - self.lastBroadcastMs

  def scanForDevices(self): 
    i2cLockActivated = self.i2c.try_lock()

    if not i2cLockActivated: 
      if self.verbose: self.msg("scanForDevices: pending lock")
      time.sleep(self.scanLockPendingNap)

    addressesFound = i2c.scan()

    self.i2c.unlock()

### end ###
