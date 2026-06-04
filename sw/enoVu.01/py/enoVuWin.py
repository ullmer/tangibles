# Enodia Vu window prototype
# Brygg Ullmer, Clemson University
# Begun 2026-06-04

from enoBase import *

class EnoVuWin(EnoBase):
  width:  int = -1
  height: int = -1

  #### constructor ####

  def __init__(self, width: int, height: int): 
    super().__init__()

    self.width  = width
    self.height = height

  #### draw ####

  def draw(self): pass

### end ###
