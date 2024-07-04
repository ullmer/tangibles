# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-06-24

from solid  import *  # load in SolidPython/SCAD support code; solid2?
from enoFRS import *

efrs = enoFRS()

backGrid  = efrs.synthPortal2DArray(10, 5)
sideGrid  = efrs.synthPortal2DArray(5,  5)

sideGridL1 = efrs.spinObj(0, 0, -90, sideGrid)
sideGridR1 = efrs.spinObj(0, 0,  90, sideGrid)

sideGridL2 = efrs.shiftObj(0, -20, 0, sideGridL1)
sideGridR2 = efrs.shiftObj(0,  20, 0, sideGridR1)

scene = backGrid + sideGridL2 + sideGridR2

efrs.renderScad('frs03.scad', scene)

### end ###

