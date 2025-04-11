#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from enoTkiButtonArray import *
from tkinter           import *

def dButtonCb(arg): print("d button callback, argument " + str(arg))

root = Tk()    # Create the root (base) window 
etba = enoTkiButtonArray(parent=root)
root.mainloop() # Start the event loop

### end ###
