# Enodia Vu Textbox prototype
# Brygg Ullmer, Clemson University
# Begun 2026-06-04

from enoBase import *

class EnoVuTbox(EnoBase):

  width:      int  = -1
  height:     int  = -1
  textStr:    str  = None
  textScale:  int  = 1
  textOffset: (int, int) = (5, 5)

  fillBox:   bool = True

  ############ constructor ############

  def __init__(self, width: int, height: int, textStr: str) -> None: 
    super().__init__()

    self.width   = width
    self.height  = height
    self.textStr = textStr

  ############ draw ############

  def draw(self): 
    try:
      self.drawBox()
      self.drawText()
    except: self.err("draw")

  ############ drawBox, drawText ############

  def drawBox(self)  -> bool: 
    self.msg('drawBox called, abstract class');  return False

  def drawText(self) -> bool: 
    self.msg('drawText called, abstract class'); return False

### end ###
