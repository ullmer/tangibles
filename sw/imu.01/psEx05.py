#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from enoTkiTicButtonArray import *
from enoEmbSerialConsole  import *
from tkinter              import *

root = Tk()    # Create the root (base) window 

etba = enoTkiTicButtonArray(parent=root, yamlFn='mm03.yaml')
eesc = enoEmbSerialConsole()

root.mainloop() # Start the event loop

### end ###
