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

  width, height       = 8, 8
  rectOutlineWidth    = 2
  x0, y0              = 50, 3
  dx, dy              = 10, 10
  rows, cols          = 2, 10
  mapCoordIdx2DispIdx = None

  ############################## constructor ##############################

  def __init__(self, oledRoot):
    self.oledRoot = oledRoot
    self.constructRectArray() 

  ############## error, message (allowing future redirection) ##############

  def err(self, msg): print("enoEDispRectArray err:", str(msg))
  def msg(self, msg): print("enoEDispRectArray msg:", str(msg))

  ############################## map coordinate x, y to index ##############################

  def constructRectArray(self): 
    if self.oledRoot is None: self.err("constructRectArrays: oledRoot uninitialized"); return
    self.mapCoordIdx2DispIdx = {}; y = self.y0

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
    outlined_rect = Rect(x=x, y=y, width=w, height=h, outline=0xFFFFFF, stroke=2)
    self.oledRoot.append(outlined_rect)

### end ###
