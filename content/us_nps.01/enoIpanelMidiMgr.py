# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time

from enoMidiController import *
from enoMidiAkai       import *
from enoIpanelMidi     import *
from enoIpanelMgr      import *

############# enodia interaction panel MIDI manager #############

class enoIpanelMidiMgr(enoIpanelMgr):

  emc     = None #enodia midi controller

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
  midiActive       = False

  midiButtonZoomToggle = 'i9'

  ipanelSidebarDict = None
  midiUnavailabilityReported  = None
  lastNotHandledControl       = None
  
  midiZoomToggleSet = False
 
  suppressRepeatNotHandledMsg = True

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    if self.autolaunchMidi: 
      try: 
        self.initMidi()
        if self.emc is not None:
          self.emc.dimMatrixSidebarAkaiApcMini()
        else: self.msg("constructor noting that midi initiation apparently unsuccessful")
        self.rightSidebarPress(0)
      except: self.err("constructor challenges with midi launch"); return None

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelMidiMgr error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelMidiMgr msg: "   + str(msgStr))

  def isZoomToggleButton(self, control):
    if control == self.midiButtonZoomToggle: return True
    return False

  ############# register interaction panel #############

  def registerIpanel(self, ipanelHandle, whichSidebarButton):
    super().registerIpanel(ipanelHandle, whichSidebarButton)

    ipanelHandle.emc                           = self.emc #possibly revisit

    if self.sidebarButtonCurrentlyActive == whichSidebarButton:
      ipanelHandle.illumCharMatrixMidi()
  
  ############# poll midi #############

  def pollMidi(self):
    if self.emc is None:
      mur = self.midiUnavailabilityReported 
      if mur is None or mur is False:
        self.msg("pollMidi: Enodia midi controller emc is not initialized")
        self.midiUnavailabilityReported = True
        return None

    self.emc.pollMidi()

  ############# midi cb #############

  def initMidi(self):
    try:
      mcn  = self.midiCtrlName     
      mcoi = self.midiCtrlOutputId 

      self.msg("initMidi (%s, %i)" % (mcn, mcoi))
      #self.emc = enoMidiController(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      self.emc = enoMidiAkai(mcn, midiCtrlOutputId=mcoi, activateOutput=True)
      self.emc.registerControls(self.midiCB)
      self.midiActive = True
    except: self.err("initMidi")
  
  ############# handle sidebar #############

  def rightSidebarPress(self, whichButton):
    if self.sidebarButtonCurrentlyActive is not None:
      self.emc.dimSidebar(self.sidebar_right, self.sidebarButtonCurrentlyActive)

    if self.verbose: self.msg("rightSidebarPress " + str(whichButton))
    self.emc.illumMatrixSidebar(self.sidebar_right, whichButton, 1)
    self.sidebarButtonCurrentlyActive = whichButton

    ripan = self.getRegisteredIpanel(whichButton)
    if ripan is not None: ripan.illumCharMatrixMidi()

  ############# midi cb #############

  def midiCB(self, control, arg): 
    try:
      if arg == 0: return #presently ignore "release event" from midi controller buttons
      if self.verbose: print("enoIpanelMidiMgr midiCB stub %s: %s" % (control, arg)) 

      if self.isSidebarButton(control):
        self.msg("sidebar button pressed") #console message, to assist interpretation
        whichSidebarButton = self.getSidebarButtonVal(control)
        self.rightSidebarPress(whichSidebarButton)
        cipan  = self.getCurrentInteractionPanel()
        cipan.isMidiGridButtonSelected = False
        cipan.illumCharMatrixMidi()

      elif self.isMatrixButton(control):
        self.msg("grid matrix button pressed") #console message, to assist interpretation
        cipan       = self.getCurrentInteractionPanel()
        coordTuple  = self.emc.mapCoord2Tuple(control)
        self.setCurrentCoord(coordTuple)
        cipan.midiButtonSelectedCoords = coordTuple
        cipan.isMidiGridButtonSelected = True
        cipan.illumCharMatrixMidi()
        cipan.screenAugmentSelectedGrid(coordTuple)
        if self.verbose: print("midiCB grid coord: " + str(coordTuple))

      elif self.isZoomToggleButton(control):
        self.zoomToggle()

      else: 
        if self.suppressRepeatNotHandledMsg and control == self.lastNotHandledControl: return
        self.lastNotHandledControl = control

        self.msg("midiCB unhandled: " + str(control))

    except: self.err("midiCB " + str(control) + ":" + str(arg)) 

  def zoomToggle(self): 
    self.msg("zoomToggle/midi activated")
    if self.midiZoomToggleSet is False:
      self.emc.illumMatrixSidebar(self.sidebar_bottom, 8, 1)
      self.midiZoomToggleSet = True 
    else:
      self.emc.illumMatrixSidebar(self.sidebar_bottom, 8, 0)
      self.midiZoomToggleSet = False
  
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
