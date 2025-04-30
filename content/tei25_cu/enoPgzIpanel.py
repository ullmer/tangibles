# Interaction panel MIDI code 
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback
from pygame import time

from enoMidiController import *
from enoMidiAkai       import *
from enoIpanelYaml     import *
from enoIpanelMidi     import *

############# enodia interaction panel midi #############

class enoPgzIpanel(enoIpanelMidi):

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ############# error, msg #############
 
  def err(self, msgStr): print("enoPgzIpanel error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoPgzIpanel msg: "   + str(msgStr))

  ############# screen augmentation of selected grid locus #############

  def screenAugmentSelectedGrid(self, coordTuple):
    try:
      i, j = coordTuple
      gridVal = self.getMatrixLocus(i, j)
      self.msg("screenAugmentSelectedGrid called, " + \
        str(coordTuple) + " " + str(gridVal))
    except: self.err("screenAugmentSelectedGrid"); return None

### end ###
