#!/usr/bin/env python

import sys, os
from pygame import time
from enoMidiController import *

#emc = enoMidiController('nu_mt3')
#emc = enoMidiController('nu_dj2go2')
#emc = enoMidiController('aka_apcmini2')

emc = enoMidiController('nov_launchpad_mk2')
#emc.registerControls(emc.debugCallback)

#emc.clearLights()
emc.rightMarginRainbow()

try:
  for i in range(8):
    for j in range(8):
      emc.setLaunchpadXYcolor(i, j, 10*i, 0, 10*j)
except: pass

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
