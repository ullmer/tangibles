# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-07-03

from solid  import *  # load in SolidPython/SCAD support code; solid2?
from enoFRS import *

efrs = enoFRS()

th = 4 #thickness, in mm

backGrid   = efrs.synthPortal2DArrayHoles(10, 5, th,  5)
sideGrid   = efrs.synthPortal2DArrayHoles( 5, 5, th,  0)
cornerGrid = efrs.synthPortal2DArrayHoles( 1, 5, th, -4)

sideGridL1 = efrs.spinObj(  0,   0, -90, sideGrid)
sideGridL2 = efrs.shiftObj(-11, -16, 0, sideGridL1)
sideGridR2 = efrs.shiftObj(89,   2,   0, sideGridL2)

cornerGridL1 = efrs.spinObj(  0,  0,  45, cornerGrid)
cornerGridL2 = efrs.shiftObj(-11, -4.7, 0, cornerGridL1)

cornerGridR1 = efrs.spinObj(  0,  0, -45, cornerGrid)
cornerGridR2 = efrs.shiftObj(74, -4.2, 0, cornerGridR1)

scene  = backGrid + sideGridL2 + sideGridR2 
scene +=          cornerGridL2 + cornerGridR2

efrs.renderScad('frs04.scad', scene)

### end ###

