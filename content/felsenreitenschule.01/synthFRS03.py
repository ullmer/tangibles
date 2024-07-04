# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-06-24

from solid  import *  # load in SolidPython/SCAD support code; solid2?
from enoFRS import *

efrs = enoFRS()

portalGrid = efrs.synthPortal2DArray(10, 5)
efrs.renderScad('frs03.scad', portalGrid)

### end ###

