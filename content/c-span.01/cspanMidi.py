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
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.super().__init__()

  ############# error, msg #############

  def err(self, msg): print("cspanMidi error: " + str(msg)); traceback.print_exc(); 
  def msg(self, msg): print("cspanMidi msg: "   + str(msg))

############# main #############

if __name__ == "__main__":
  cm = cspanMidi()
  r  = cm.mapCharToColor('B')
  r  = cm.mapCharToColor('J')

### end ###
 
