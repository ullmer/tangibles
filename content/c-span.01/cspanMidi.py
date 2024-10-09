# C-SPAN MIDI code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time
from enoMidiController import *

############# cspan midi #############

class cspanMidi:

  tagFn = 'cspan-tags.yaml'
  tagYd = None
  tags  = None

  midiCtrlName     = 'aka_apcmini2'
  midiCtrlOutputId = 4

  ############# constructor #############

  def __init__(self, controllerName, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    if self.tagFn is not None: self.loadYaml()

    self.initMidi()
    self.midiIllumDefault()

  ############# error, msg #############

  def err(self, msg): print("cspanMidi error: " + str(msg)); traceback.print_exc(); 
  def msg(self, msg): print("cspanMidi msg: "   + str(msg))

  ############# load yaml #############

  def loadYaml(self):
    self.tags  = []

    try:
      yf         = open(self.tagFn, 'rt')
      self.tagYd = yaml.safe_load(yf)

      ytags      = self.tagYd['tags']
      for tag in ytags: self.tags.append(tag)
    except: self.err("loadYaml")

  ############# getCharMatrix #############

  def getCharMatrix(self):
    try:
      result = self.tagYd['interactionPanel']['charMatrix']
      return result
    except: self.err("getCharMatrix")

  ############# midi cb #############

  def initMidi(self):
    try:
      mcn  = self.midiCtrlName     
      mcoi = self.midiCtrlOutputId 

      self.emc = enoMidiController(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      self.emc.registerControls(self.midiCB)
    except: self.err("initMidi")

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
