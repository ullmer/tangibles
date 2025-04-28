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

  def midiCB(control, arg): 
    global tags, tagIdx

    if arg == 0: return #ignore pad release

    print("midiCB stub %s: %s" % (tags[tagIdx], str(control)))
  
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

  while True:
    emc.pollMidi()
    time.wait(100)

### end ###
