# Enodia core Clemson-variant board, v01
# By Brygg Ullmer, Clemson University
# Begun 2025-01

from enoCoreC01 import *
from enoEDispRectArray import *

ec1 = enoCoreC01()
ec1.oledClear()
ec1.displayText("go")
ec1.neopixLightStr("PO") #BY, etc.

eedra1 = enoEDispRectArray(ec1.oledRoot)
eedra1.setEl(1, 2)
eedra1.setEl(4, 1)

### end ###
