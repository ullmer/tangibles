# Enodia core Clemson-variant board, v01
# By Brygg Ullmer, Clemson University
# Begun 2025-01

# Some code excerpts draw from https://learn.adafruit.com/adafruit-oled-featherwing/circuitpython-usage
#  and CoPilot

import board, terminalio, displayio, neopixel
import adafruit_displayio_ssd1306

from adafruit_display_text        import label
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font         import bitmap_font

############################## Enodia Core/C v01 ##############################

class enoEDispRectArray: #EDisp: embedded display (as we'll wish variants for traditional and 3D displays)

  oledRoot = None

  width,  height        = 9, 9
  width2, height2       = 7, 7 #usually width-rectOutlineWidth*2, h-row*2
  rectOutlineWidth      = 1
  x0, y0                = 30, 8
  dx, dy                = 10, 10
  rows, cols            = 2, 10
  mapCoordIdx2DispIdx   = None #outer outlined-rect
  mapCoordIdx2DispInner = None #inner filled-rect

  ############################## constructor ##############################

  def __init__(self, oledRoot):
    self.oledRoot = oledRoot
    self.constructRectArray() 

  ############## error, message (allowing future redirection) ##############

  def err(self, msg): print("enoEDispRectArray err:", str(msg))
  def msg(self, msg): print("enoEDispRectArray msg:", str(msg))

  ############################## map coordinate x, y to index ##############################

  def setEl(self, x, y): 
    if self.mapCoordIdx2DispInner is None: self.err("setEl: class uninitialized"); return

    idx = self.mapXY2Idx(x,y)
    if idx in self.mapCoordIdx2DispInner: return #already set

    x1 = self.x0 + (self.dx * (x-1)) + self.rectOutlineWidth
    y1 = self.y0 + (self.dy * (y-1)) + self.rectOutlineWidth

    self.drawFilledRect(x1, y1, self.width2, self.height2)
    self.mapCoordIdx2DispInner[idx] = len(self.oledRoot) - 1

  ############################## map coordinate x, y to index ##############################

  def clearEl(self, x, y): 
    if self.mapCoordIdx2DispInner is None: self.err("setEl: class uninitialized"); return

    idx = self.mapXY2Idx(x,y)
    if idx not in self.mapCoordIdx2DispInner: return #already unset
    di = self.mapCoordIdx2DispInner[idx]
    del self.oledRoot[di]

    orl


    # we then probably need to decrement addresses for remaining cached addresses greater than di
    
  ############################## map coordinate x, y to index ##############################

  def constructRectArray(self): 
    if self.oledRoot is None: self.err("constructRectArrays: oledRoot uninitialized"); return

    self.mapCoordIdx2DispIdx   = {}; y = self.y0
    self.mapCoordIdx2DispInner = {}

    for i in range(self.rows):
      x = self.x0
      for j in range(self.cols):
        idx = self.mapXY2Idx(j,i)
        self.mapCoordIdx2DispIdx[idx] = self.drawOutlinedRect(x, y, self.width, self.height)
        x += self.dx
      y += self.dy  

  ############################## map coordinate x, y to index ##############################

  def mapXY2Idx(self, x, y): return (x * self.cols) + y

  ############################## oled : draw rectangles ##############################

  def drawFilledRect(self, x, y, w, h):
    if self.oledRoot is None: self.err("drawFilledRect: oledRoot uninitialized"); return
    filled_rect = Rect(x=x, y=y, width=w, height=h, fill=0xFFFFFF)
    self.oledRoot.append(filled_rect)

  def drawOutlinedRect(self, x, y, w, h):
    if self.oledRoot is None: self.err("drawOutlinedRect: oledRoot uninitialized"); return
    strk = self.rectOutlineWidth
    outlined_rect = Rect(x=x, y=y, width=w, height=h, outline=0xFFFFFF, stroke=strk)
    self.oledRoot.append(outlined_rect)

### end ###
