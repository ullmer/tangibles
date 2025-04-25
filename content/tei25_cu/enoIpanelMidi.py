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

  singleKeyToAbbrev   = None
  singleKeyToColorVal = None 

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

  def isAllUpperAlpha(self, text):
    try:    result = (text.isalpha() and text.isupper()); return result
    except: return False

  def notAllUpperAlpha(self, text):
    try: result = (not text.isalpha() or not text.isupper()); return result
    except: return False

  ############# map character to color #############

  def registerColormap(self, illumMap, charMap): 
    if (not isinstance(charMap,  dict) or not isinstance(illumMap, dict)):
      self.msg("registerColormap: arguments illumMap and charMap must both be of type dict"); return None

    self.singleKeyToAbbrev   = {}
    self.singleKeyToColorVal = {}

    self.msg("urg")
    for charMapKey in charMap:
      if self.notAllUpperAlpha(charMapKey): continue # ignore elements if not all uppercase & alpha
      self.msg("charMapKey:" + str(charMapKey))
      charMapVal = charMap[charMapKey]
      self.singleKeyToAbbrev[charMapKey] = charMapVal

      if charMapVal not in illumMap: self.msg("registerColorMap: charMapVal not in illumMap: " + str(charMapVal)); continue
      illumVal = illumMap[charMapVal]
      self.singleKeyToColorVal[charMapVal] = illumVal

      charMapValLower = charMapVal.tolower()
      if charMapValLower not in illumMap: self.msg("registerColorMap: cmvLower not in illumMap: " + str(charMapValLower)); continue
      illumValLower = illumMap[charMapValLower]
      self.singleKeyToColorVal[charMapValLower] = illumValLower
    
    #first, map all upper-case single-characters to two characters
    #then,  map two characters to (initially, single-value) mappings for upper- and lowercase charmaps

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
      if self.singleKeyToColorVal is None: 
        if self.tagYd is None: self.msg("mapCharToColor: tagYd is none!"); return None

      illumMap = self.tagYd['midiIllum'][self.midiCtrlName]
      charMap  = self.tagYd['interactionPanel']['charMap']
      self.registerColormap(illumMap, charMap) 
    except:
      self.err("mapCharToColor")

  def mapCharToColor0(self, tagChar):  #first variant
    #different devices represent color in very different ways. try to accomodate.
    try:
      tag = self.mapCharToCategory(tagChar)
      if tag is None: self.err('mapCharToColor: mapCharToCategory returned no result'); return

      if self.verbose: self.msg("mapCharToColor : tag " + str(tag))

      dcl = self.getDeviceColorLookup(self.midiCtrlName)

      if dcl is None:  self.msg("mapCharToColor: get device color lookup returns None."); return None

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
          
          illumFunc(i, j, color)

    except: self.err("illumCharMatrixMidi"); return None
   
  ############# illuminate matrix x, y, color#############

  def illumMatrixXYC(self, x, y, color):
    if self.midiCtrlName == 'aka_apcmini2': self.illumMatrixXYCAkaiApcMini(x,y,color)

  def illumMatrixXYCAkaiApcMini(self, x, y, color):
    try:
      addr = self.cols * (y - 7) + x
      if self.emc is None: self.msg("illumMatrixXYCAkaiApcMini: emc not initialized"); return None
      self.emc.midiOut.note_on(addr, color, 3)
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

  cm = enoIpanelMidi(tagFn = 'us-bea.yaml')
  m  = cm.getCharMatrix()
  cm.illumCharMatrixMidi()
  print(m)

#while True:
#  emc.pollMidi()
#  time.wait(100)

### end ###
