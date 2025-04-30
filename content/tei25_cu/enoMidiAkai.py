# Interaction panel MIDI code 
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time
from enoMidiController import *

############# enodia interaction panel midi #############

class enoMidiAkai(enoMidiController):

  verbose = False
  #verbose = True

  tagCharToColor = None
  autolaunchMidi = True

  singleKey2Abbrev   = None
  singleKey2ColorVal = None 
  abbrev2singleKey   = None
  abbrev2ColorVal    = None 

  rows, cols     = 8, 8
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

  def __init__(self, controllerName, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__(controllerName)

  ############# error, msg #############

  def err(self, msgStr): print("enoMidiAkai error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoMidiAkai msg: "   + str(msgStr))

  ############# illuminate matrix x, y, color #############

  def illumMatrixXYC(self, x, y, color, brightness):
    if self.midiCtrlName == 'aka_apcmini2' or \
       self.midiCtrlName == 'akaiApcMiniMk2': self.illumMatrixXYCAkaiApcMini(x,y,color,brightness)

  def illumMatrixXYCAkaiApcMini(self, x, y, color, brightness=3):
    try:
      #self.msg("imxyaam " + str(x) + " " + str(y))
      #addr = self.cols * (y - 7) + x
      addr = self.cols * (7 - y) + x
      if self.verbose: self.msg("illumMatrixXYCAkaiApcMini " + str(addr) + " " + str(color))
      if addr is None or color is None: 
        self.msg("illumMatrixXYCAkaiApMini args " + str(addr) + " " + str(color))
      else:                             
        self.midiOut.note_on(addr, color, brightness)
    except: self.err("illumMatrixXYCAkaiApcMini")
  
  ############# midi cb #############

  def midiCB(self, control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    if self.verbose: print("midiCB stub %s: %s" % (tags[tagIdx], str(control)))
  
  ############# dim matrix sidebar #############

  def dimSidebar(self, side=True, idx=True):
    if self.midiCtrlName == 'aka_apcmini2' or \
       self.midiCtrlName == 'akaiApcMiniMk2': 
         self.dimMatrixSidebarAkaiApcMini(side, idx)

  def dimMatrixSidebarAkaiApcMini(self, side=True, idx=True):
    if self.verbose: 
      self.msg("dimMatrixSidebarAkaiApcMini " + str(side) + " " + str(idx)) 

    if side is True and idx is True:
      for i in range(100, 108): self.midiOut.note_on(i, 0)
      for i in range(112, 120): self.midiOut.note_on(i, 0)
      return True

    if side == self.sidebar_right:
      if idx is True: #all on
        for i in range(112, 120): self.midiOut.note_on(i, 0)
      elif idx >= 0 and idx < 8: 
        idx2 = 112+idx; self.midiOut.note_on(idx2, 0)
      else: 
        self.msg("dimMatrixSidebarAkaiApcMini right called with invalid index: " + str(idx))
        return None

  ############# illuminate matrix sidebar #############

  def illumMatrixSidebar(self, side=True, idx=True, color=1):
    if self.midiCtrlName == 'aka_apcmini2' or \
       self.midiCtrlName == 'akaiApcMiniMk2': 
         self.illumMatrixSidebarAkaiApcMini(side, idx, color)

  def illumMatrixSidebarAkaiApcMini(self, side=True, idx=True, color=1):
    try:
      if self.verbose: self.msg("illumMatrixSideAkaiApcMini")

      if side is True and idx is True: #all on
         for i in range(100, 108): self.midiOut.note_on(i, 1, color)
         for i in range(112, 120): self.midiOut.note_on(i, 1, color)

      if side == self.sidebar_bottom:
        if idx is True: #all on
          for i in range(100, 108): self.midiOut.note_on(i, 1, color)
        elif idx >= 0 and idx < 8: 
          idx2 = 100+idx; self.midiOut.note_on(idx2, 1, color)
        else: 
          self.msg("illumMatrixSidebarAkaiApcMini bottom called with invalid index: " + str(idx))
          return None

      if side == self.sidebar_right:
        if idx is True: #all on
          for i in range(112, 120): self.midiOut.note_on(i, 1)
        elif idx >= 0 and idx < 8: 
          idx2 = 112+idx; self.midiOut.note_on(idx2, 1)
        else: 
          self.msg("illumMatrixSidebarAkaiApcMini right called with invalid index: " + str(idx))
          return None

      #self.midiOut.note_on(100, 1)
      #self.midiOut.note_on(112, 1)

    except: self.err("illumMatrixSidebarAkaiApcMini")
 #thanks: https://forum.bome.com/t/new-akai-pro-apc-mini-mk2-initial-led-mapping-summary/4752

### end ###
