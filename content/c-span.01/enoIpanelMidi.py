# Interaction panel MIDI code 
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time
from enoMidiController import *
from enoIpanel import *

############# cspan midi #############

class enoIpanelMidi(enoIpanel):

  emc   = None #enodia midi controller

  tagCharToColor = None
  autolaunchMidi = True

  deviceColorLookups = {
    'aka_apcmini2' : ['interactionPanel', 'akaiColorMap']
  }

  midiCtrlName     = 'aka_apcmini2'
  midiCtrlOutputId = 4

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.super()

    if self.autolaunchMidi: 
      self.initMidi()
      self.illumDefaultMidi()

  ############# error, msg #############

  def err(self, msg): print("enoIpanelMidi error: " + str(msg)); traceback.print_exc(); 
  def msg(self, msg): print("enoIpanelMidi msg: "   + str(msg))

  ############# get device color lookup #############

  def getDeviceColorLookup(self, midiCtrlName):
  
    try:
      if midiCtrlName not in self.deviceColorLookups:
        self.err("getDeviceColorLookup: midi controller name not in device color lookups"); return None

      dcl = self.deviceColorLookups[midiCtrlName]

      if type(dcl) is not list: return dcl

      result = self.tagYd #we're working with a list; iterate through it

      for el in dcl:
        if el not in result: 
          self.err("getDeviceColorLookup iteration through " + str(dcl) + " fails"); return None

        result = result[el] # awkward, best refined, but hopefully will work

      return result
    except: self.err("getDeviceColorLookup " + str(midiCtrlName)); return None

  ############# getCharMatrix #############

  def mapCharToColor(self, tagChar): #different devices represent color in very different ways. try to accomodate.
    try:
      if self.verbose: self.msg("mapCharToColor " + str(tagChar))
      if self.tagCharToColor is None: self.tagCharToColor = {}

      if tagChar in self.tagCharToColor: return self.tagCharToColor[tagChar] #caching key to performance

      try:    cm = self.tagYd['interactionPanel']['charMap']
      except: self.err('mapCharToColor: problem accessing charMap in YAML descriptor'); return None

      if tagChar not in cm: self.err('mapCharToColor not finding character ' + str(tagChar)); return None

      cme = cm[tagChar]
      tag = cme[0]

      if self.verbose: self.msg("mapCharToColor : tag " + str(tag))

      dcl = self.getDeviceColorLookup(self.midiCtrlName)

      if self.verbose: self.msg("mapCharToColor: dcl: " + str(dcl))

      if tag not in dcl: 
        self.err("mapCharToColor: device color lookup " + str(dcl) + " not found in yaml " + self.tagFn)
        return None

      color = dcl[tag]
      if self.verbose: self.msg("mapCharToColor result: " + str(color))

      self.tagCharToColor[tagChar] = color
      return color

    except: self.err("mapCharToColor")

  ############# midi cb #############

  def initMidi(self):
    try:
      mcn  = self.midiCtrlName     
      mcoi = self.midiCtrlOutputId 

      self.msg("initMidi (%s, %i)" % (mcn, mcoi))

      self.emc = enoMidiController(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      #self.emc.registerControls(self.midiCB)
    except: self.err("initMidi")

  ############# illuminate default midi #############

  def illumDefaultMidi(self):
    try:
      illumFunc = None
      if self.midiCtrlName == 'aka_apcmini2': illumFunc = self.illumMatrixXYCAkaiApcMini

      if illumFunc is None:
        self.msg("illumDefaultMidi: no controller function identified"); return

      if self.emc is None: self.err("illumDefaultMidi: self.emc is none!")

      m = self.getCharMatrix()
      mrows = m.splitlines()
      for j in range(self.rows):
        row = mrows[j]
        for i in range(self.cols):
          try:    mch   = row[i]
          except: self.err("illumDefaultMidi error on %i, %i" % (i,j)); continue
          color = self.mapCharToColor(mch)
          
          illumFunc(i, j, color)

    except: self.err("illumDefaultMidi"); return None
   
  ############# illuminate matrix x, y, color#############

  def illumMatrixXYC(self, x, y, color):
    if self.midiCtrlName == 'aka_apcmini2': self.illumMatrixXYCAkaiApcMini(x,y,color)

  def illumMatrixXYCAkaiApcMini(self, x, y, color):
     
    try:
      addr = self.cols * (y - 7) + x

      self.emc.midiOut.note_on(addr, color, 3)
    except: self.err("illumMatrixXYCAkaiApcMini")

  ############# midi cb #############

  def midiCB(control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    print("cspan midiCB %s: %s" % (tags[tagIdx], str(control)))
  
############# main #############

if __name__ == "__main__":
  cm = enoIpanelMidi(tagFn = 'cspan-tags.yaml')
  r  = cm.mapCharToColor('B')
  r  = cm.mapCharToColor('J')
  m  = cm.getCharMatrix()
  print(m)

#while True:
#  emc.pollMidi()
#  time.wait(100)

### end ###
