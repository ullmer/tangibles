#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from enoTkiButtonArray import *
from enoEmbSerialConsole  import *
from tkinter              import *

class enoTkiEmbButtonArray(enoTkiButtonArray, enoEmbSerialConsole): #inherits methods from both
  def __init__(self, **kwargs):  #this and subsequent two lines each include ~"opaque magic"
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()           #call the constructors for both enoTkiButtonArray and enoEmbSerialConsole

root = Tk()    # Create the root (base) window 

etba = enoTkiEmbButtonArray(parent=root, yamlFn='ps05.yaml')

root.mainloop() # Start the event loop

### end ###
