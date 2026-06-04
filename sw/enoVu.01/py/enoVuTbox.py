# Enodia Vu Textbox prototype
# Brygg Ullmer, Clemson University
# Begun 2026-06-04

from enoBase import *

def EnoVuTbox(EnoBase):

  width:   int = -1
  height:  int = -1
  textStr: str = None

  def __init__(self, width: int, height: int, textStr: str): 
    super().__init__()

    self.width   = width
    self.height  = height
    self.textStr = textStr

  def draw(self): pass 

### end ###
