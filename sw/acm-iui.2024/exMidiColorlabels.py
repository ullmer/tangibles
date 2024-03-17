#Example of enoMidiController functionality for Novation Launchpad
#Brygg Ullmer, Clemson University
#Begun 2023-09-06

import sys, os
from pygame import time
from enoMidiController import *
from functools   import partial

#### callback function ####

def buttonCB(emc, control, arg):
  x, y    = emc.addr2coord(control)
  r, g, b = [63, 63, 63]
  emc.setLaunchpadXYColor(x, y, r, g, b)

#### labelLaunchpad####

def labelLaunchpad(emc):

  for i in range(4): emc.setLaunchpadXYColor(i, 0, 13, 13, 13)

  for j in range(4):
    for i in [0, 4]: emc.setLaunchpadXYColor(i, j+1, 8,   8, 8)
    for i in [1, 5]: emc.setLaunchpadXYColor(i, j+1, 0,   8, 2)
    for i in [2, 6]: emc.setLaunchpadXYColor(i, j+1, 10, 10, 0)
    for i in [3, 7]: emc.setLaunchpadXYColor(i, j+1, 15,  5, 0)

  emc.setLaunchpadXYColor(0, 5, 8, 8, 8)
  emc.setLaunchpadXYColor(1, 5, 0, 8, 2)

  for i in [2, 7]: emc.setLaunchpadXYColor(i, 5, 4, 4, 4)

  emc.setLaunchpadXYColor(3, 5,  0, 12,  0) #na
  emc.setLaunchpadXYColor(4, 5,  0,  0, 12) #eu
  emc.setLaunchpadXYColor(5, 5, 14,  0,  0) #as
  emc.setLaunchpadXYColor(6, 5, 14, 14,  0) #me

  for j in range(3):
    for i in [0, 2, 4, 6]: emc.setLaunchpadXYColor(i, j+6, 0, 0, 8)
    for i in [1, 3, 5, 7]: emc.setLaunchpadXYColor(i, j+6, 8, 8, 8)

#### main ####

emc = enoMidiController('nov_launchpad_x')
#emc = enoMidiController('nov_launchpad_mk2')
emc.clearLights()

labelLaunchpad(emc)

#emc.rightMarginRainbow()
emc.registerExternalCB(buttonCB)

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
