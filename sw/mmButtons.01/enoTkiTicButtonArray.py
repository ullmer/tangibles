#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter
# https://github.com/jphalip/ticlib

from enoTkiButtonArray import *
from ticlib            import TicUSB
import traceback

class enoTkiTicButtonArray(enoTkiButtonArray): # Intersects enoTkiButtonArray with Pololu TIC stepper support

  ticCtrl      = None
  positions    = [500, 300, 800, 0]
  ticHwPresent = False
  ticHwActive  = False
    
  def msg(self, msg): print("enoTkiTicButtonArray msg: " + str(msg)) #allows later redirection

  ########## initialize TIC ########## 

  def hwPresent(self): 
    if self.ticHwPresent: return True
    return False

  ########## initialize TIC ########## 

  def initTic(self):
    if self.hwPresent()
      try:
        self.ticCtrl = TicUSB()

        self.ticCtrl.halt_and_set_position(0)
        self.ticCtrl.energize()
        self.ticCtrl.exit_safe_start()
        self.ticHwActive = True

      except:
        self.msg("initTic error:"); traceback.print_exc()

    else: self.msg("initTic called (without hardware)")

  ########## initialize TIC ########## 
  
  def gotoTargetPosAbs(self, targetPos):

    if self.hwPresent() and self.ticHwActive():
      self.ticCtrl.set_target_position(targetPos)
    else: self.msg("gotoTargetPosAbs (w/o hw): " + str(targetPos))

  ########## stop TIC ########## 

  def stopTic(self):
    if self.hwPresent() and self.ticHwActive:
      try:
        self.ticCtrl.deenergize()
        self.ticCtrl.enter_safe_start()
        self.ticHwActive = False
      except:
        self.msg("stopTic error:"); traceback.print_exc()
    
#while tic.get_current_position() != tic.get_target_position():
#    sleep(0.1)

### end ###
