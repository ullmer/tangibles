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

from board import *

#from board import PA02, PA03, PA04, PA05, PA06, PA07, PA08, PA09, PA10,  #ptc/capacitive lines
#                  PA11, PA14, PA15, PA16, PA17, PA18, PA19, PA20, PA21, 
#                  PA22, PA23, PA24, PA25, PA27, PA28, PA30, PA31

GND, 3V3, VIN = [None]*3 #hopefully allows these to be referenced in pcb_j2 list
  
############################## Enodia Core/C v01 ##############################

class enoCoreC01:

  i2c, display_bus, display, oledRoot = [None]*4 #initialize all to None
  color_bitmap, color_palette, font   = [None]*3
  text_area, neopix, touchSensors     = [None]*3

  pixel_pin       = board.D4
  num_pixels      = 2
  displayOledByDefault = True #if True, displays defaultOledText on initiation

  defaultOledText      = "hello"
  defaultFont1    = "/fonts/ostrich-sans-black-36.pcf"
  defaultNeopixColor = (3,1,0)
  colorDict = {'R': (3,0,0), 'G': (0,3,0), 'B': (0,0,3), 'O': (3,1,0), 'P': (3,0,3), 
               'W': (2,2,2), 'Y': (3,3,0)}

  touch_pins_cp = [PA02, PA03, PA04, PA05, PA06, PA07, PA08, PA09, PA10, PA11, PA14, PA15, PA16, 
                   PA17, PA18, PA19, PA20, PA21, PA22, PA23, PA24, PA25, PA27, PA28, PA30, PA31]

  pcb_j2     = [PA05, PA06, PA04, PA07, PB09, PB12, PB08, PB13, PB07, PB14, PB06, PB15, PB05,
                PA16, PB04, PA17, None, PA18, None, PA23, PB16, PA22, MOSI, PA21, SCK,  PB00, 
                MISO, GND,  PA15, SCL,   3V3, SDA] # last ~8 entries should be checked again

  #pcb_j2_ptc = "++++.........+.+"

  touch_pins = [PA05, PA06, PA04, PA07, PB09, PB12, PB08, PB13, PB07, PB14, PB06, PB15, PB05,
                PA16, PB04, PA17, PA18, PA23, PB16, PA22, PA21, PB00]


  ############################## constructor ##############################

  def __init__(self):
    self.initOled() 
    self.initNeopix()
    self.initTouch()

  ############## error, message (allowing future redirection) ##############

  def err(self, msg): print("enoCore01 err:", str(msg))
  def msg(self, msg): print("enoCore01 msg:", str(msg))

  ############################## initiate oled ##############################

  def initOled(self):
    displayio.release_displays()

    self.i2c         = board.I2C()  # uses board.SCL and board.SDA
    self.display_bus = adafruit_displayio_ssd1306.I2CDisplayBus(self.i2c, device_address=0x3C)
    self.display     = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=32)

    # Make the display context
    self.oledRoot           = displayio.Group() #root display group
    self.display.root_group = self.oledRoot

    self.color_bitmap     = displayio.Bitmap(128, 32, 1)
    self.color_palette    = displayio.Palette(1)
    self.color_palette[0] = 0xFFFFFF  # White
    self.font             = self.loadFont(self.defaultFont1)
    if self.displayOledByDefault: self.displayText(self.defaultOledText)

  ############################## oled : draw rectangles ##############################

  def drawFilledRect(self):
    filled_rect = Rect(x=10, y=10, width=50, height=30, fill=0xFFFFFF)
    self.oledRoot.append(filled_rect)

  def drawOutlinedRect(self):
    outlined_rect = Rect(x=70, y=10, width=50, height=30, outline=0xFFFFFF, stroke=2)
    self.oledRoot.append(outlined_rect)

  ############################## initiate oled ##############################

  def initTouch(self):
    self.touchSensors = []
    for pin in self.touch_pins: self.touchSensors.append(touchio.TouchIn(pin))

  ############################## loadFont ##############################

  def loadFont(self, fontFn):
    result = bitmap_font.load_font(fontFn)
    return result

  ############################## display text ##############################

  def displayText(self, txt):
    self.text_area = label.Label(self.font, text=txt, color=0xFFFFFF, x=1, y=16)
    self.oledRoot.append(self.text_area)

  ############################## clear oled ##############################

  def oledClear(self):
    if self.oledRoot is None: self.err("clearOled: oledRoot uninitialized"); return
    while len(self.oledRoot) > 0: self.oledRoot.pop() 

  ############################## neopixel init ##############################

  def initNeopix(self):
    self.neopix = neopixel.NeoPixel(self.pixel_pin, self.num_pixels)
    self.neopixFill(self.defaultNeopixColor)

  ############################## neopixel fill ##############################

  def neopixFill(self, color):
    if self.neopix is None: self.err("neopixFill: not yet initialized"); return
    self.neopix.fill(color)

  #################### neopixel light pixels per a string of colormapped characters ####################

  def neopixLightStr(self, colorStr, mult=1):
    if self.neopix is None:           self.err("neopixLightStr: not yet initialized"); return
    if not isinstance(colorStr, str): self.err("neopixLightStr: colorStr argument is not a string"); return 

    n = len(colorStr)
    if n > self.num_pixels: n = self.num_pixels

    for i in range(n):
      ledColorChr = colorStr[i]
      if ledColorChr not in self.colorDict: self.err("neopixLightStr: char " + str(i) + " not in colormap; ignoring"); continue
      color = self.colorDict[ledColorChr]

      if mult==1: self.neopix[i] = color
      else:       c2 = (color[0]*mult, color[1]*mult, color[2]*mult); self.neopix[i]=c2

### end ###
