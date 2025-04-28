# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time
from enoMidiController import *

############# enodia interaction panel MIDI manager #############

class enoIpanelMidiMgr:

  emc     = None #enodia midi controller
  verbose = False
  #verbose = True

  sidebar_bottom = 1
  sidebar_right  = 2

  deviceColorLookups = {
    'akaiApcMiniMk2' : ['interactionPanel', 'akaiColorMap']
  }

  midiBrightness   = None
  midiCtrlName     = 'akaiApcMiniMk2'
  midiCtrlOutputId = 4

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    if self.autolaunchMidi: 
      self.initMidi()
      self.dimMatrixSidebarAkaiApcMini()

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelMidiMgr error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelMidiMgr msg: "   + str(msgStr))

  ############# poll midi #############

  def pollMidi(self):
    if self.emc is None:
      self.msg("pollMidi: Enodia midi controller emc is not initialized"); return None

    self.emc.pollMidi()

  ############# midi cb #############

  def initMidi(self):
    try:
      mcn  = self.midiCtrlName     
      mcoi = self.midiCtrlOutputId 

      self.msg("initMidi (%s, %i)" % (mcn, mcoi))
      self.emc = enoMidiController(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      self.emc.registerControls(self.midiCB)
    except: self.err("initMidi")
  
  ############# dim matrix sidebar #############

  def dimSidebar(self, side=True, idx=True):
    if self.midiCtrlName == 'aka_apcmini2' or \
       self.midiCtrlName == 'akaiApcMiniMk2': 
         self.dimMatrixSidebarAkaiApcMini(side, idx)

  def dimMatrixSidebarAkaiApcMini(self, side=True, idx=True):
    if self.verbose: 
      self.msg("dimMatrixSidebarAkaiApcMini " + str(side) + " " + str(idx)) 
    if side is True and idx is True:
      for i in range(100, 108): self.emc.midiOut.note_on(i, 0)
      for i in range(112, 120): self.emc.midiOut.note_on(i, 0)
      return True

    if side == self.sidebar_right:
      if idx is True: #all on
        for i in range(112, 120): self.emc.midiOut.note_on(i, 0)
      elif idx >= 0 and idx < 8: 
        idx2 = 112+idx; self.emc.midiOut.note_on(idx2, 0)
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
      if self.emc is None: 
        self.msg("illumMatrixXYCAkaiApcMini: emc not initialized"); return None
      if self.verbose: self.msg("illumMatrixSideAkaiApcMini")

      if side is True and idx is True: #all on
         for i in range(100, 108): self.emc.midiOut.note_on(i, 1, color)
         for i in range(112, 120): self.emc.midiOut.note_on(i, 1, color)

      if side == self.sidebar_bottom:
        if idx is True: #all on
          for i in range(100, 108): self.emc.midiOut.note_on(i, 1, color)
        elif idx >= 0 and idx < 8: 
          idx2 = 100+idx; self.emc.midiOut.note_on(idx2, 1, color)
        else: 
          self.msg("illumMatrixSidebarAkaiApcMini bottom called with invalid index: " + str(idx))
          return None

      if side == self.sidebar_right:
        if idx is True: #all on
          for i in range(112, 120): self.emc.midiOut.note_on(i, 1)
        elif idx >= 0 and idx < 8: 
          idx2 = 112+idx; self.emc.midiOut.note_on(idx2, 1)
        else: 
          self.msg("illumMatrixSidebarAkaiApcMini right called with invalid index: " + str(idx))
          return None

      #self.emc.midiOut.note_on(100, 1)
      #self.emc.midiOut.note_on(112, 1)

    except: self.err("illumMatrixSidebarAkaiApcMini")
 #thanks: https://forum.bome.com/t/new-akai-pro-apc-mini-mk2-initial-led-mapping-summary/4752

  ############# handle sidebar #############

  def rightSidebarPress(self, whichButton):
    if self.sidebarButtonCurrentlyActive is not None:
      self.dimSidebar(self.sidebar_right, self.sidebarButtonCurrentlyActive)

    if self.verbose: self.msg("rightSidebarPress " + str(whichButton))
    self.illumMatrixSidebar(self.sidebar_right, whichButton, 1)
    self.sidebarButtonCurrentlyActive = whichButton

  ############# midi cb #############

  def midiCB(self, control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    if self.verbose: print("enoIpanelMidiMgr midiCB stub %s: %s" % (control, arg))

    if len(control) == 2: #standard
      if control[1] == '9': #right sidebar candidate
        if control[0] >= 'a' and control[0] <= 'h':
          whichSidebar = ord(control[0]) - ord('a')
          self.rightSidebarPress(whichSidebar)
  
############# main #############

if __name__ == "__main__":
  print("=" * 70)
  #eimm = enoIpanelMidiMgr(tagFn = 'cspan-tags.yaml', casePaired=False)
  eimm = enoIpanelMidiMgr(tagFn = 'us-bea.yaml',     casePaired=True)

  while True:
    eimm.pollMidi()
    time.wait(100)

### end ###
