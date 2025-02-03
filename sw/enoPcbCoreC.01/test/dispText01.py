# Code draws heavily from https://learn.adafruit.com/adafruit-oled-featherwing/circuitpython-usage

import board
import terminalio
import displayio       
import adafruit_displayio_ssd1306
from   adafruit_display_text import label
from   adafruit_bitmap_font  import bitmap_font

displayio.release_displays()

i2c = board.I2C()  # uses board.SCL and board.SDA
display_bus = adafruit_displayio_ssd1306.I2CDisplayBus(i2c, device_address=0x3C)
display     = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(128, 32, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
#splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(118, 24, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
#splash.append(inner_sprite)

#font = bitmap_font.load_font("/fonts/ostrich_sans_bold_24.pcf")
#font = bitmap_font.load_font("/fonts/ostrich_sans_bold-36.pcf")
#font = bitmap_font.load_font("/fonts/ostrich_sans_bold_60.pcf")
font = bitmap_font.load_font("/fonts/ostrich-sans-black-36.pcf")
text_area = label.Label(font, text="Welcome", color=0xFFFFFF, x=1, y=16)

#text_area = label.Label(terminalio.FONT, text="Welcome", color=0xFFFF00, x=28, y=15)
splash.append(text_area)

### end ###
