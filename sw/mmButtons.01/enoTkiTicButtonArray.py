#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter
# https://github.com/jphalip/ticlib

from enoTkiButtonArray import *
from ticlib            import TicUSB

class enoTkiTicButtonArray(enoTkiButtonArray): # Intersects enoTkiButtonArray with Pololu TIC stepper support

  ticCtrl   = None
  positions = [500, 300, 800, 0]

  ########## initialize TIC ########## 

  def initTic(self):
    try:
      self.ticCtrl = TicUSB()

      self.ticCtrl.halt_and_set_position(0)
      self.ticCtrl.energize()
      self.ticCtrl.exit_safe_start()

    except:

  ########## initialize TIC ########## 
  
  def gotoTargetPosAbs(self, targetPos):

    self.ticCtrl.set_target_position(targetPos)

  ########## stop TIC ########## 

  def stopTic(self):
    self.ticCtrl.deenergize()
    self.ticCtrl.enter_safe_start()
    
#while tic.get_current_position() != tic.get_target_position():
#    sleep(0.1)
  

### end ###
