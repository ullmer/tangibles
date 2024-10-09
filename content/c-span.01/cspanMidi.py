# C-SPAN MIDI code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

cspan-tags.yaml
#!/usr/bin/env python

import sys, os, yaml
from pygame import time


import sys; sys.path.append("..")
from enoMidiController import *

yfn = '../cspan-tags.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

ytags = yd['tags']
tags = []
for tag in ytags: tags.append(tag)
tagIdx = 0

#emc = enoMidiController('nu_mt3')
#emc = enoMidiController('nu_dj2go2')
#emc = enoMidiController('nov_launchpad_mk2')

def midiCB(control, arg): 
  global tags, tagIdx

  if arg == 0: return #ignore pad release

  print("%s: %s" % (tags[tagIdx], str(control)))
  tagIdx += 1
  print(tags[tagIdx])

emc = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)
emc.registerControls(midiCB)

for i in range(64): emc.midiOut.note_on(i, i, 3)

print(tags[tagIdx])

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
#!/usr/bin/env python

import sys, os
from pygame import time

import sys; sys.path.append("..")
from enoMidiController import *

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
