# Enodia Vu Textbox prototype
# Brygg Ullmer, Clemson University
# Begun 2026-06-04

from enoBase import *

class EnoVuTbox(EnoBase):

  width:     int = -1
  height:    int = -1
  textStr:   str = None
  textScale: int = 1

  def __init__(self, width: int, height: int, textStr: str) -> None: 
    super().__init__()

    self.width   = width
    self.height  = height
    self.textStr = textStr

  def draw(self): pass 

### end ###
