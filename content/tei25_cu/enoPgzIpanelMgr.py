# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback
from pygame import time

from enoIpanelMidiMgr import *

class enoPgzIpanelMgr: pass

############# main #############

eimm = enoIpanelMidiMgr()

if __name__ == "__main__":
  print("=" * 70)

  eim1 = enoIpanelMidi(tagFn = 'us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
  eim2 = enoIpanelMidi(tagFn = 'cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

  eimm.registerIpanel(eim1, 0) #bootstrapping logic, to be reworked
  eimm.registerIpanel(eim2, 1)

def update(): eimm.pollMidi()

### end ###
