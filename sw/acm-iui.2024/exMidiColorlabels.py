#Example of enoMidiController functionality for Novation Launchpad
#Brygg Ullmer, Clemson University
#Begun 2023-09-06

import sys, os
from pygame import time
from enoMidiController import *
from functools   import partial

#### callback function ####

def painterCB(emc, control, arg):
  if control[0] == 'm': #margin button
    whichMarginKey = control[1]

    if emc.isRightMargin(whichMarginKey):
      color = emc.getRightMarginColor(whichMarginKey)
      emc.setActiveColor(color)
      emc.topMarginFadedColor(color)

    if emc.isTopMargin(whichMarginKey):
      color = emc.getTopMarginColor(whichMarginKey)
      emc.setActiveColor(color)
      
  else: 
    x, y    = emc.addr2coord(control)
    r, g, b = emc.getActiveColor()
    emc.setLaunchpadXYColor(x, y, r, g, b)

#### labelLaunchpad####

def labelLaunchpad(emc):
  for j in range(8):
    for i in [1, 3, 5, 7]: emc.setLaunchpadXYColor(i, j, 10, 10, 0)
    for i in [0, 2, 4, 6]: emc.setLaunchpadXYColor(i, j, 63, 63, 0)

#### main ####

emc = enoMidiController('nov_launchpad_x')
#emc = enoMidiController('nov_launchpad_mk2')
emc.clearLights()

labelLaunchpad(emc)

#emc.rightMarginRainbow()
#emc.registerExternalCB(painterCB)

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
