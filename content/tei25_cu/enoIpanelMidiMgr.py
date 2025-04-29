# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time

from enoMidiController import *
from enoIpanelMidi     import *

############# enodia interaction panel MIDI manager #############

class enoIpanelMidiMgr:

  emc     = None #enodia midi controller
  verbose = False
  #verbose = True

  autolaunchMidi = True

  sidebar_bottom = 1
  sidebar_right  = 2
  sidebarButtonCurrentlyActive = None

  deviceColorLookups = {
    'akaiApcMiniMk2' : ['interactionPanel', 'akaiColorMap']
  }

  midiBrightness   = None
  midiCtrlName     = 'akaiApcMiniMk2'
  midiCtrlOutputId = 4

  ipanelSidebarDict = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    if self.autolaunchMidi: 
      self.initMidi()
      self.dimMatrixSidebarAkaiApcMini()
      self.rightSidebarPress(0)

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelMidiMgr error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelMidiMgr msg: "   + str(msgStr))

  ############# register interaction panel #############

  def registerIpanel(self, ipanelHandle, whichSidebarButton):
    if self.ipanelSidebarDict is None:
      self.ipanelSidebarDict = {}

    self.ipanelSidebarDict[whichSidebarButton] = ipanelHandle
    ipanelHandle.emc                           = self.emc #possibly revisit

    if self.sidebarButtonCurrentlyActive == whichSidebarButton:
      ipanelHandle.illumCharMatrixMidi()
  
  ############# get registered interaction panel #############

  def getRegisteredIpanel(self, whichSidebarButton):
    if self.ipanelSidebarDict is None:                   return None
    if whichSidebarButton not in self.ipanelSidebarDict: return None
    result = self.ipanelSidebarDict[whichSidebarButton]
    return result

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
  
  ############# handle sidebar #############

  def rightSidebarPress(self, whichButton):
    if self.sidebarButtonCurrentlyActive is not None:
      self.dimSidebar(self.sidebar_right, self.sidebarButtonCurrentlyActive)

    if self.verbose: self.msg("rightSidebarPress " + str(whichButton))
    self.illumMatrixSidebar(self.sidebar_right, whichButton, 1)
    self.sidebarButtonCurrentlyActive = whichButton

    ripan = self.getRegisteredIpanel(whichButton)
    if ripan is not None: ripan.illumCharMatrixMidi()

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
  eim1 = enoIpanelMidi(tagFn = 'us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
  eim2 = enoIpanelMidi(tagFn = 'cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

  eimm = enoIpanelMidiMgr()
  eimm.registerIpanel(eim1, 0) #bootstrapping logic, to be reworked
  eimm.registerIpanel(eim2, 1)

  while True:
    eimm.pollMidi()
    time.wait(100)

### end ###
