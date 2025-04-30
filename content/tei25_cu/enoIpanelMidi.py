# Interaction panel MIDI code 
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time
from enoMidiController import *
from enoMidiAkai       import *
from enoIpanelYaml     import *

############# enodia interaction panel midi #############

class enoIpanelMidi(enoIpanelYaml):

  emc     = None #enodia midi controller
  verbose = False
  #verbose = True

  tagCharToColor = None
  autolaunchMidi = True

  singleKey2Abbrev   = None
  singleKey2ColorVal = None 
  abbrev2singleKey   = None
  abbrev2ColorVal    = None 

  illumFunc   = None
  coord2color = None

  sidebar_bottom = 1
  sidebar_right  = 2

  deviceColorLookups = {
    'akaiApcMiniMk2' : ['interactionPanel', 'akaiColorMap']
  }

  midiBrightness     = None

  midiCtrlName     = 'akaiApcMiniMk2'
  midiCtrlOutputId = 4
  casePaired       = False

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    if self.autolaunchMidi: 
      self.initMidi()
      self.illumCharMatrixMidi()
      self.emc.dimMatrixSidebarAkaiApcMini()

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelMidi error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelMidi msg: "   + str(msgStr))

  ############# poll midi #############

  def pollMidi(self):
    if self.emc is None:
      self.msg("pollMidi: Enodia midi controller emc is not initialized"); return None

    self.emc.pollMidi()

  ############# get device color lookup #############

  def getDeviceColorLookup(self, midiCtrlName):
  
    try:
      if midiCtrlName not in self.deviceColorLookups:
        self.err("getDeviceColorLookup: midi controller name not in device color lookups")
        return None

      dcl = self.deviceColorLookups[midiCtrlName]

      if type(dcl) is not list: return dcl

      result = self.tagYd #we're working with a list; iterate through it

      for el in dcl:
        if el not in result: 
          self.err("getDeviceColorLookup iteration through " + str(dcl) + " fails"); return None

        result = result[el] # awkward, best refined, but hopefully will work

      return result
    except: self.err("getDeviceColorLookup " + str(midiCtrlName)); return None

  ############# helpers #############

  def isAllUpperAlpha(self, text):
    try:    result = (text.isalpha() and text.isupper()); return result
    except: return False

  def notAllUpperAlpha(self, text):
    try: result = (not text.isalpha() or not text.isupper()); return result
    except: return False

  ############# map character to color #############

  def registerColormap(self, colorMap, charMap): 
    if self.singleKey2Abbrev is not None: 
      self.msg("registerColormap called, but skta already populated"); return None

    if (not isinstance(charMap,  dict) or not isinstance(colorMap, dict)):
      self.msg("registerColormap: arguments colorMap and charMap must both be of type dict"); return None

    self.singleKey2Abbrev   = {}
    self.abbrev2ColorVal    = {}
    self.abbrev2singleKey   = {}
    self.singleKey2ColorVal = {}

    if self.verbose: self.msg("rcm" + str(charMap) + " || " + str(colorMap))
    for charMapKey in charMap:
      if self.casePaired and self.notAllUpperAlpha(charMapKey): 
        continue # ignore elements if not all uppercase & alpha
      abbrev    = charMap[charMapKey][0]
      if abbrev not in colorMap: 
        if charMapKey in colorMap: abbrev = charMapKey
        else: 
          self.msg("registerColormap: abbrev, charMapKey not in colorMap: " + \
                   str(abbrev) + str(colorMap)); continue

      illumVal  = colorMap[abbrev]
      self.abbrev2singleKey[abbrev]     = charMapKey

      charMapKeyLower = charMapKey.lower()  #this is abbrev, not char
      self.singleKey2ColorVal[charMapKey]      = illumVal[0]
      if len(illumVal)>1: self.singleKey2ColorVal[charMapKeyLower] = illumVal[1]
    
    if self.verbose: self.msg("singleKey2ColorVal: " + str(self.singleKey2ColorVal))

  ############# map character to color #############

  def mapCharToColor(self, tagChar): 
    try:
      if self.singleKey2ColorVal is None: 
        if self.tagYd is None: self.msg("mapCharToColor: tagYd is none!"); return None

      midiMap   = self.tagYd['interactionPanel']['midi'][self.midiCtrlName]
      colorMap  = midiMap['illum']
      brightMap = midiMap['brightness']

      charMap  = self.tagYd['interactionPanel']['charMap']

      #if self.verbose: self.msg("mapCharToColor " + str(colorMap) + " :: " + str(charMap))
      if self.singleKey2Abbrev is None: self.registerColormap(colorMap, charMap) 

      #if self.verbose: 
      #  self.msg("mapCharToColor foo: " + str(self.singleKey2ColorVal) + "|" + str(tagChar))

      if tagChar not in self.singleKey2ColorVal: return None

      cv = self.singleKey2ColorVal[tagChar]
      return cv

    except:
      self.err("mapCharToColor")

  ############# midi cb #############

  def initMidi(self):
    try:
      mcn  = self.midiCtrlName     
      mcoi = self.midiCtrlOutputId 

      self.msg("initMidi (%s, %i)" % (mcn, mcoi))
      #self.emc = enoMidiController(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      self.emc = enoMidiAkai(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      self.emc.registerControls(self.midiCB)
    except: self.err("initMidi")

  ############# illuminate default midi #############

  def cacheCharMatrixColors(self):
    if self.verbose: print("cacheCharMatrixMidi: ")

    try:
      if self.coord2color is None:
        self.coord2color = {}

      m = self.getCharMatrix()
      mrows = m.splitlines()
      for j in range(self.rows):
        row = mrows[j]
        for i in range(self.cols):
          try:    mch   = row[i]
          except: self.err("cacheCharMatrixColors error on %i, %i" % (i,j)); continue
 
          if mch == '.': self.coord2color[(i,j)] = 0
          else: 
            color, coord = self.mapCharToColor(mch), (i, j)
            if self.verbose: self.msg('cacheCharMatrixColors: ' + \
              str(mch) + ":" + str(color) + ":" + str(coord))
            if color is not None: self.coord2color[coord] = color

      if self.verbose: print("c2c: " + str(self.coord2color))
    except: self.err("cacheCharMatrixColors"); return None

  ############# initiate illumination func #############

  def initIllumFunc(self):
      if self.midiCtrlName == 'aka_apcmini2':   self.illumFunc = self.emc.illumMatrixXYCAkaiApcMini
      if self.midiCtrlName == 'akaiApcMiniMk2': self.illumFunc = self.emc.illumMatrixXYCAkaiApcMini

      if self.illumFunc is None:
        self.msg("illumCharMatrixMidi: no controller function identified"); return

      if self.emc is None: self.err("illumCharMatrixMidi: self.emc is none!")

  ############# illuminate default midi #############

  def illumCharMatrixMidi(self):
    try:
      if self.illumFunc is None:   self.initIllumFunc()
      if self.coord2color is None: self.cacheCharMatrixColors()

      if self.verbose: print("illumCharMatrixMidi: " + str(self.coord2color))

      for j in range(self.rows):
        for i in range(self.cols):
          coord = (i,j)
          if coord in self.coord2color:
            color = self.coord2color[coord]
            self.illumFunc(i, j, color)

    except: self.err("illumCharMatrixColors"); return None
   
  ############# midi cb #############

  def midiCB(self, control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    if self.verbose: print("midiCB stub %s: %s" % (tags[tagIdx], str(control)))
  
############# main #############

if __name__ == "__main__":
  #cm = enoIpanelMidi(tagFn = 'cspan-tags.yaml')
  #cm = enoIpanelMidi(tagFn = 'us-bea.yaml', autolaunchMidi=False)

  print("=" * 70)
  #cm = enoIpanelMidi(tagFn = 'cspan-tags.yaml', casePaired=False)
  cm = enoIpanelMidi(tagFn = 'us-bea.yaml',     casePaired=True)
  m  = cm.getCharMatrix()
  cm.illumCharMatrixMidi()
  print(m)

#while True:
#  emc.pollMidi()
#  time.wait(100)

### end ###
