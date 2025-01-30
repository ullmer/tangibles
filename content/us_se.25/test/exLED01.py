# http://multiwingspan.co.uk/pico.php?page=dotstar
# https://docs.micropython.org/en/latest/rp2/quickref.html

from machine import SPI,Pin
from time import sleep
import micropython_dotstar as DS

spi=SPI(0, sck=Pin(18), mosi=Pin(19))
d=DS.DotStar(spi, 14)

d.fill((1,   0, 0))
d.fill((255, 0, 0))

