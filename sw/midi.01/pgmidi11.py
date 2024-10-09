#!/usr/bin/env python

import sys, os
from pygame import time
from enoMidiController import *
from time import sleep

#emc = enoMidiController('nu_mt3')
#emc = enoMidiController('nu_dj2go2')
#emc = enoMidiController('nov_launchpad_mk2')

def midiCB(control, arg): print("midicb: ", str(control), str(arg))

emc = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)
emc.registerControls(midiCB)

for i in range(64): emc.midiOut.note_on(i, i, 3)

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
