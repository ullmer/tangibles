# Simple LED + capacitive example relative to US Southeast interaction panel
# Brygg Ullmer, Clemson University
# Begun 2025-01-29

# http://multiwingspan.co.uk/pico.php?page=dotstar
# https://github.com/mcauser/micropython-mpr121
# https://docs.micropython.org/en/latest/rp2/quickref.html

from machine import SPI,I2C,Pin
from time import sleep
import micropython_dotstar as DS

spi=SPI(0, sck=Pin(18), mosi=Pin(19))
d=DS.DotStar(spi, 14)

d.fill((1,   0, 0))
d.fill((255, 0, 0))

i2c=I2C(0, scl=Pin(5), sda=Pin(4))
mpr=mpr121.MPR121(i2c, 0x5A)
mpr.touched()

### end ###
