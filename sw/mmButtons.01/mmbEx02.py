#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from mmButtons import *
from tkinter   import *

class enoTkiButtonArrayVariant(enoTkiButtonArray):
  def dButtonCb(arg): print("d button callback, argument " + str(arg))

root = Tk()    # Create the root (base) window 
etba = enoTkiButtonArrayVariant(parent=root, yamlFn='mm02.yaml')

root.mainloop() # Start the event loop

### end ###
