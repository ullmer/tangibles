# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time
from enoIpanelMidi import *

############# Enodia interaction panel MIDI manager #############

class enoIpanelMidiMgr(enoIpanelMidi):

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ############# msg, error #############

  def msg(self, msgStr): print("enoIpanelMidiMgr msg: "   + str(msgStr))
  def err(self, msgStr): print("enoIpanelMidiMgr error: " + str(msgStr)); traceback.print_exc(); 

  ############# midi cb #############

  def midiCB(self, control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    #print("midiCB stub %s: %s" % (tags[tagIdx], str(control)))
    print("midiCB stub %s: %s" % (control, arg))
  
############# main #############

if __name__ == "__main__":
  print("=" * 70)
  #eimm = enoIpanelMidiMgr(tagFn = 'cspan-tags.yaml', casePaired=False)
  eimm = enoIpanelMidiMgr(tagFn = 'us-bea.yaml',     casePaired=True)

  #m    = eimm.getCharMatrix()
  #cm.illumCharMatrixMidi()
  #print(m)

  while True:
    eimm.pollMidi()
    time.wait(100)

### end ###
