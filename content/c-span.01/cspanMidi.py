# C-SPAN MIDI code 
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time

from enoMidiController import *
from enoIpanelMidi import *

############# cspan midi #############

def cspanMidi(enoIpanelMidi):
  cspTagFn = 'cspan-tags.yaml'
  
  ############# constructor #############

  def __init__(self, **kwargs):
    self.tagFn = cspTagFn

    super.__init__(kwargs)

  ############# error, msg #############

  def err(self, msg): print("cspanMidi error: " + str(msg)); traceback.print_exc(); 
  def msg(self, msg): print("cspanMidi msg: "   + str(msg))

### end ###
 
