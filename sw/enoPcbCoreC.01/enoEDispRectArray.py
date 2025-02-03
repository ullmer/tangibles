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

  rectDimension       = 8
  rectOutlineWidth    = 2
  startPos            = (50, 3)
  dx, dy              = 10, 10
  rows, cols          = 2, 10
  mapCoordIdx2DispIdx = None

  ############################## constructor ##############################

  def __init__(self, oledRoot):
    self.constructRectArray() 

  ############## error, message (allowing future redirection) ##############

  def err(self, msg): print("enoEDispRectArray err:", str(msg))
  def msg(self, msg): print("enoEDispRectArray msg:", str(msg))

  ############################## map coordinate x, y to index ##############################

  def mapXY2Idx(self, x, y): return (x * self.cols) + y

  ############################## map coordinate x, y to index ##############################

  def mapXY2Idx(self, x, y): return (x * self.cols) + y

  ############################## oled : draw rectangles ##############################

  def drawFilledRect(self):
    if self.oledRoot is None: self.err("drawFilledRect: oledRoot uninitialized"); return
    filled_rect = Rect(x=10, y=10, width=50, height=30, fill=0xFFFFFF)
    self.oledRoot.append(filled_rect)

  def drawOutlinedRect(self):
    if self.oledRoot is None: self.err("drawOutlinedRect: oledRoot uninitialized"); return
    outlined_rect = Rect(x=70, y=10, width=50, height=30, outline=0xFFFFFF, stroke=2)
    self.oledRoot.append(outlined_rect)

### end ###
