# C-SPAN MIDI code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml
from pygame import time
from enoMidiController import *


class cspanMidi:

  tagFn = 'cspan-tags.yaml'
  tagYd = None
  tags  = None

  def loadYaml(self):
    self.tags  = []
    yf         = open(self.tagFn, 'rt')
    self.tagYd = yaml.safe_load(yf)

    ytags      = self.tagYd['tags']
    for tag in ytags: self.tags.append(tag)


  def midiCB(control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    print("cspan midiCB %s: %s" % (tags[tagIdx], str(control)))

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
