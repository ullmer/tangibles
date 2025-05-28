#drawing from:
# https://learn.adafruit.com/adafruit-2-9-eink-display-breakouts-and-featherwings/circuitpython-usage#
# https://www.waveshare.com/wiki/Pico-ePaper-2.9-B 
# https://docs.circuitpython.org/projects/ssd1680/en/latest/
# Copilot (2025-05-18)

import time

import board
import busio
import displayio
import fourwire

#import adafruit_il0373
#from adafruit_epd.ssd1680 import Adafruit_SSD1680
import ep

displayio.release_displays()

spi = busio.SPI(board.GP10, board.GP11)
epd_cs   = board.GP9
epd_dc   = board.GP8
epd_rst  = board.GP12
epd_busy = board.GP13

#display_bus = fourwire.FourWire(spi, command=epd_dc, chip_select=epd_cs, baudrate=1000000)

display_bus = fourwire.FourWire(spi, command=epd_dc, chip_select=epd_cs, reset=epd_rst)

#display = Adafruit_SSD1680(
#    display_bus, width=296, height=128, rotation=270, busy_pin=epd_busy
#)

#display = Adafruit_SSD1680(display_bus, 296, 128, epd_busy)

#display = Adafruit_SSD1680(display_bus, 296, 128, 0, busy_pin=epd_busy)
display = ep.SSD1680(display_bus, width=296, height=128, busy_pin=epd_busy)

splash = displayio.Group()

# Create a text label
text = "Hello, World!"
text_area = label.Label(terminalio.FONT, text=text, color=0x000000, x=10, y=64)
splash.append(text_area)

# Show it on the display
display.show(splash)
display.refresh()

print("Displayed 'Hello, World!'")

