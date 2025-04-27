# Interaction panel MIDI code 
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time
from enoMidiController import *
from enoIpanelYaml import *

############# cspan midi #############

class enoIpanelMidi(enoIpanelYaml):

  emc   = None #enodia midi controller

  tagCharToColor = None
  autolaunchMidi = True

  singleKey2Abbrev   = None
  singleKey2ColorVal = None 
  abbrev2singleKey   = None
  abbrev2ColorVal    = None 

  deviceColorLookups = {
    'akaiApcMiniMk2' : ['interactionPanel', 'akaiColorMap']
  }

  midiCtrlName     = 'akaiApcMiniMk2'
  midiCtrlOutputId = 4

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    if self.autolaunchMidi: 
      self.initMidi()
      self.illumCharMatrixMidi()

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelMidi error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelMidi msg: "   + str(msgStr))

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

  def isAllUpperAlpha(self, text):
    try:    result = (text.isalpha() and text.isupper()); return result
    except: return False

  def notAllUpperAlpha(self, text):
    try: result = (not text.isalpha() or not text.isupper()); return result
    except: return False

  ############# map character to color #############

  def registerColormap(self, illumMap, charMap): 
    if self.singleKey2Abbrev is not None: 
      self.msg("registerColormap called, but skta already populated"); return None

    if (not isinstance(charMap,  dict) or not isinstance(illumMap, dict)):
      self.msg("registerColormap: arguments illumMap and charMap must both be of type dict"); return None

    self.singleKey2Abbrev   = {}
    self.abbrev2ColorVal    = {}
    self.abbrev2singleKey   = {}
    self.singleKey2ColorVal = {}

    self.msg("urg" + str(charMap) + " || " + str(illumMap))
    for charMapKey in charMap:
      if self.notAllUpperAlpha(charMapKey): continue # ignore elements if not all uppercase & alpha
      #self.msg("charMapKey:" + str(charMapKey))
      #charMapVal = charMap[charMapKey][0]
      abbrev    = charMap[charMapKey][0]
      if abbrev not in illumMap: 
        self.msg("registerColormap: abbrev not in illumMap: " + str(abbrev) + str(illumMap)); continue

      illumVal  = illumMap[abbrev]
      self.abbrev2singleKey[abbrev]     = charMapKey

      charMapKeyLower = charMapKey.lower()  #this is abbrev, not char
      self.singleKey2ColorVal[charMapKey]      = illumVal[0]
      self.singleKey2ColorVal[charMapKeyLower] = illumVal[1]
    
    #first, map all upper-case single-characters to two characters
    #then,  map two characters to (initially, single-value) mappings for upper- and lowercase charmaps

    print("singleKey2ColorVal: " + str(self.singleKey2ColorVal))

#midiIllum:
#  akaiApcMiniMk2: {rm: [9, 10], me: [61, 62], gl: [43, 45], se: [5, 7], ne: [41, 38], pl: [27, 19]}
#
#interactionPanel:
#  charMap:
#    {N: [NE], n: [vt, nh, me, ct, ri, ma],
#     M: [ME], m: [pa, ny, nj, de, dc, md],

  ############# map character to color #############

  def mapCharToColor(self, tagChar): 
    try:
      if self.singleKey2ColorVal is None: 
        if self.tagYd is None: self.msg("mapCharToColor: tagYd is none!"); return None

      illumMap = self.tagYd['midiIllum'][self.midiCtrlName]
      charMap  = self.tagYd['interactionPanel']['charMap']

      #self.msg("mapCharToColor " + str(illumMap) + " :: " + str(charMap))
      if self.singleKey2Abbrev is None: self.registerColormap(illumMap, charMap) 

      #self.msg("mapCharToColor foo: " + str(self.singleKey2ColorVal) + "|" + str(tagChar))

      if tagChar not in self.singleKey2ColorVal: return None

      cv = self.singleKey2ColorVal[tagChar]
      #cv = self.abbrev2ColorVal[tagChar]
      return cv

    except:
      self.err("mapCharToColor")

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

  def illumCharMatrixMidi(self):
    try:
      illumFunc = None
      if self.midiCtrlName == 'aka_apcmini2':   illumFunc = self.illumMatrixXYCAkaiApcMini
      if self.midiCtrlName == 'akaiApcMiniMk2': illumFunc = self.illumMatrixXYCAkaiApcMini

      if illumFunc is None:
        self.msg("illumCharMatrixMidi: no controller function identified"); return

      if self.emc is None: self.err("illumCharMatrixMidi: self.emc is none!")

      m = self.getCharMatrix()
      mrows = m.splitlines()
      for j in range(self.rows):
        row = mrows[j]
        for i in range(self.cols):
          try:    mch   = row[i]
          except: self.err("illumCharMatrixMidi error on %i, %i" % (i,j)); continue
          color = self.mapCharToColor(mch)

          if color is not None: illumFunc(i, j, color)

    except: self.err("illumCharMatrixMidi"); return None
   
  ############# illuminate matrix x, y, color#############

  def illumMatrixXYC(self, x, y, color):
    if self.midiCtrlName == 'aka_apcmini2': self.illumMatrixXYCAkaiApcMini(x,y,color)

  def illumMatrixXYCAkaiApcMini(self, x, y, color):
    try:
      self.msg("imxyaam " + str(x) + " " + str(y))
      #addr = self.cols * (y - 7) + x
      addr = self.cols * (7 - y) + x
      if self.emc is None: self.msg("illumMatrixXYCAkaiApcMini: emc not initialized"); return None
      self.msg("illumMatrixXYCAkaiApcMini " + str(addr) + " " + str(color))
      if addr is None or color is None: self.msg("illumMatrixXYCAkaiApMini args " + str(addr) + " " + str(color))
      else:                             self.emc.midiOut.note_on(addr, color, 3)
    except: self.err("illumMatrixXYCAkaiApcMini")

  ############# midi cb #############

  def midiCB(control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    print("cspan midiCB %s: %s" % (tags[tagIdx], str(control)))
  
############# main #############

if __name__ == "__main__":
  #cm = enoIpanelMidi(tagFn = 'cspan-tags.yaml')
  #r  = cm.mapCharToColor('B')
  #r  = cm.mapCharToColor('J')

  #cm = enoIpanelMidi(tagFn = 'us-bea.yaml', autolaunchMidi=False)

  print("=" * 70)
  cm = enoIpanelMidi(tagFn = 'us-bea.yaml')
  m  = cm.getCharMatrix()
  cm.illumCharMatrixMidi()
  print(m)

#while True:
#  emc.pollMidi()
#  time.wait(100)

### end ###
