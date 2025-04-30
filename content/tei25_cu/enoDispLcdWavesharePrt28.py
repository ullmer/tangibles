import board, busio
import terminalio, displayio, digitalio
import time, os
import sdcardio
import storage
import sys
import fourwire  # Updated import for FourWire

from adafruit_display_text import label
from adafruit_bitmap_font  import bitmap_font
from adafruit_st7789       import ST7789

# initial code from https://markmcgookin.com/2023/01/11/using-the-waveshare-pico-restouch-lcd-2-8-screen-with-circuitpython/
#  updated for CircuitPython 9 by CoPilot 

class enoDispLcdWavesharePrt28:
  display  = None
  splash   = None
  led      = None
  color_bitmap  = None
  color_palette = None
  bg_sprite     = None
  font01Fn      = '/fonts/SairaCondensed-Regular.bdf'
  font01        = None
  fontScale     = 1 #with terminalio, was 3 with example code

  colorYellow = 0xFFFF00
  colorRed    = 0xFF0000
  colorBlue   = 0x0000FF

  def __init__(self):
    self.initBoard()
    self.loadFonts()
    #self.displayTest1("testing")
    self.displayTest2()

  def loadFonts(self):
    if self.font01Fn is not None:
      self.font01 = bitmap_font.load_font(self.font01Fn)

  def initBoard(self):
    self.led = digitalio.DigitalInOut(board.LED) # onboard LED
    self.led.direction = digitalio.Direction.OUTPUT
    
    displayio.release_displays() # Release any resources currently in use for the displays
    
    tft_dc  = board.GP8
    tft_cs  = board.GP9
    tft_rst = board.GP15
    
    tft_bl = digitalio.DigitalInOut(board.GP13)
    tft_bl.direction = digitalio.Direction.OUTPUT
    tft_bl.value = True
    
    spi = busio.SPI(board.GP10, board.GP11, board.GP12) # Clock, MOSI, MISO
    print(str(spi.frequency))
    
    # Updated to use fourwire.FourWire
    display_bus = fourwire.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
    self.display     = ST7789(display_bus, width=320, height=240, rotation=90)
    
    # Make the display context
    self.splash = displayio.Group()
    self.display.root_group = self.splash  # Updated to use root_group
    
  def displayTest2(self):
    # Define colors
    # Create rectangles
    rect1 = displayio.Bitmap(100, 80, 1)
    rect1_palette = displayio.Palette(1)
    rect1_palette[0] = self.colorYellow
    rect1_sprite = displayio.TileGrid(rect1, pixel_shader=rect1_palette, x=5, y=5)
    
    rect2 = displayio.Bitmap(100, 80, 1)
    rect2_palette = displayio.Palette(1)
    rect2_palette[0] = self.colorRed
    rect2_sprite = displayio.TileGrid(rect2, pixel_shader=rect2_palette, x=5, y=110)
    
    rect3 = displayio.Bitmap(100, 80, 1)
    rect3_palette = displayio.Palette(1)
    rect3_palette[0] = self.colorBlue
    rect3_sprite = displayio.TileGrid(rect3, pixel_shader=rect3_palette, x=5, y=220)
    
    # Add rectangles to the display context
    self.splash.append(rect1_sprite)
    self.splash.append(rect2_sprite)
    self.splash.append(rect3_sprite)

  def displayTest1(self, displaytext):
    self.color_bitmap     = displayio.Bitmap(320, 240, 1)
    self.color_palette    = displayio.Palette(1)
    self.color_palette[0] = 0x00FF00  # Bright Green
    
    self.bg_sprite = displayio.TileGrid(self.color_bitmap, pixel_shader=self.color_palette, x=0, y=0)
    self.splash.append(self.bg_sprite)
    
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(280, 200, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0xAA0088  # Purple
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
    self.splash.append(inner_sprite)
    
    # Draw a label
    text_group = displayio.Group(scale=self.fontScale, x=57, y=120)
    text = displaytext
    
    if self.font01 is not None: f = self.font01
    else:                       f = terminalio.FONT

    text_area = label.Label(f, text=text, color=0xFFFF00)
    text_group.append(text_area)  # Subgroup for text scaling
    self.splash.append(text_group)
    
  def cycleLed(self):
    count = 0
    last_print = time.monotonic()
    while True:
      current = time.monotonic()
        
      if current - last_print >= 1.0:
         last_print = current
            
         #print("Loop " + str(count))
         count = count + 1

         if self.led.value == True: self.led.value = False
         else:                      self.led.value = True

edlwp = enoDispLcdWavesharePrt28()
edlwp.cycleLed()

### end ###
