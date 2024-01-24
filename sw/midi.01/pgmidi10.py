#!/usr/bin/env python

import sys, os
from pygame import time
from enoMidiController import *

#emc = enoMidiController('nu_mt3')
#emc = enoMidiController('nu_dj2go2')
emc = enoMidiController('aka_apcmini2')
emc.registerControls(emc.debugCallback)

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
