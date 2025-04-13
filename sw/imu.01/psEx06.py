#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from enoTkiButtonArray import *
from enoEmbSerialConsole  import *
from tkinter              import *
import time

class enoTkiEmbButtonArray(enoTkiButtonArray, enoEmbSerialConsole): #inherits methods from both
  def __init__(self, **kwargs):  
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    enoTkiButtonArray.__init__(self)        
    enoEmbSerialConsole.__init__(self)     

  def readIMUMulti(self, arg=None):
    self.sendCommand("ejs.readIMU(50)")
    while True: 
      self.readSerial()
      time.sleep(.05)

root = Tk()    # Create the root (base) window 
etba = enoTkiEmbButtonArray(parent=root, yamlFn='ps06.yaml')

root.mainloop() # Start the event loop

### end ###
