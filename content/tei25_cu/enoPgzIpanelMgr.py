# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time

from enoIpanelMidiMgr import *

############# enodia pygame zero interaction panel manager #############

class enoPgzIpanelMgr(enoIpanelMidiMgr): 
  matrixImgFn    = None
  matrixImgActor = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

############# main #############

epim = enoPgzIpanelMgr()

print("=" * 70)

eim1 = enoIpanelMidi(tagFn = 'us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
eim2 = enoIpanelMidi(tagFn = 'cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

epim.registerIpanel(eim1, 0) #bootstrapping logic, to be reworked
epim.registerIpanel(eim2, 1)

def update(): epim.pollMidi()

### end ###
