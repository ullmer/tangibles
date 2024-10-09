# C-SPAN MIDI code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml
from pygame import time
from enoMidiController import *

############# cspan midi #############

class cspanMidi:

  tagFn = 'cspan-tags.yaml'
  tagYd = None
  tags  = None

  midiCtrlName     = 'aka_apcmini2
  midiCtrlOutputId = 4

  ############# constructor #############

  def __init__(self, controllerName, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    if self.tagFn is not None: self.loadYaml()

    self.initMidi()
    self.midiIllumDefault()

  ############# load yaml #############

  def loadYaml(self):
    self.tags  = []
    yf         = open(self.tagFn, 'rt')
    self.tagYd = yaml.safe_load(yf)

    ytags      = self.tagYd['tags']
    for tag in ytags: self.tags.append(tag)

  ############# midi cb #############

  def initMidi(self):
    mcn  = self.midiCtrlName     
    mcoi = self.midiCtrlOutputId 

    self.emc = enoMidiController(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
    self.emc.registerControls(self.midiCB)

  ############# midi illum default #############

  def midiIllumDefault(self):

    for i in range(64): emc.midiOut.note_on(i, i, 3)

  ############# midi cb #############

  def midiCB(control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    print("cspan midiCB %s: %s" % (tags[tagIdx], str(control)))

#while True:
#  emc.pollMidi()
#  time.wait(100)

### end ###
