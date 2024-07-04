# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-06-24

from solid  import *  # load in SolidPython/SCAD support code; solid2?
from enoFRS import *

efrs = enoFRS()

backGrid  = efrs.synthPortal2DArray(10, 5)
sideGrid  = efrs.synthPortal2DArray(5,  5)
sideGridL = efrs.spinObj(sideGrid)

efrs.renderScad('frs03.scad', portalGrid)

### end ###

