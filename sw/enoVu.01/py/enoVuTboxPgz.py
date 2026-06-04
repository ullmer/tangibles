# Enodia Vu Textbox :pgzero backend prototype
# Brygg Ullmer, Clemson University
# Begun 2026-06-04

from enoVuTbox import *

class EnoVuTboxPgz(EnoVuTbox):
  textColor  = (255, 255, 255)
  textAlpha  = .7
  fontName   = "barlow_condensed_extralight"
  fontSize   = 32

  ######## constructor ######## 

  def __init__(self, width: int, height: int, textStr: str) -> None: 
    super().__init__(width, height, textStr)

  ######## drawBox ######## 

  def drawBox(self, screen) -> bool:

  ######## drawText ######## 

  def drawText(self, screen) -> bool:

    try:
      tstr = self.textStr
  
      if tstr is None: 
        if self.verbose: self.msg('drawText called, no text to be drawn')
  
      fn, fs     = self.fontName, self.fontSize
      tox1, toy1 = self.textOffset
  
      bx, by  = self.basePos
      x,  y   = bx+tox1, by+toy1
      ta, tc  = self.textAlpha, self.textColor
  
      screen.draw.text(tstr, pos=(x,y), alpha=ta, color=tc, 
                       fontname=fn, fontsize=fs)

      return True
    except: self.err("drawText"); return False

### end ###
