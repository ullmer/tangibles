#!/usr/bin/env python

import sys, os
from pygame import time
from enoMidiController import *
from time import sleep

#emc = enoMidiController('nu_mt3')
#emc = enoMidiController('nu_dj2go2')
#emc = enoMidiController('nov_launchpad_mk2')


emc = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)
emc.registerControls(emc.debugCallback)

#emc.clearLights()
#emc.rightMarginRainbow()

#try:
#  for i in range(8):
#    for j in range(8):
#      emc.setLaunchpadXYcolor(i, j, 5*i, 0, 5*j)
#except: pass

#pygame.midi.init()
#i = pygame.midi.Input(1)
#o = pygame.midi.Output(4)
#for i in range(64): o.note_on(i, i, 3)

sleep(1)
for i in range(64): emc.midiOut(i, i, 3)

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
