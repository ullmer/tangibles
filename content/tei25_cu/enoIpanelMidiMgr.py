# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time
from enoIpanelMidi import *

############# Enodia interaction panel MIDI manager #############

class enoIpanelMidiMgr(enoIpanelMidi):
  sidebarButtonCurrentlyActive = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ############# msg, error #############

  def msg(self, msgStr): print("enoIpanelMidiMgr msg: "   + str(msgStr))
  def err(self, msgStr): print("enoIpanelMidiMgr error: " + str(msgStr)); traceback.print_exc(); 

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

    #print("midiCB stub %s: %s" % (tags[tagIdx], str(control)))
    print("enoIpanelMidiMgr midiCB stub %s: %s" % (control, arg))

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
