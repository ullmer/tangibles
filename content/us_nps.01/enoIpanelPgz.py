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

class enoIpanelPgz(enoIpanelMidi):
  screen       = None #these two lines probably merit refactoring
  pgzIpanelMgr = None
  transparentImgVal        = .3
  transparencyAnimDuration = .5
  transparencyAnimHandle   = None
  transparencyAnimTween    = 'accel_decel'

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ############# error, msg #############
 
  def err(self, msgStr): print("enoIpanelPgz error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelPgz msg: "   + str(msgStr))

  ############# screen augmentation of selected grid locus #############

  def screenAugmentSelectedGrid(self, coordTuple): 
    try:
      i, j = coordTuple
      gridVal = self.getMatrixLocus(i, j)
      if self.verbose: self.msg("screenAugmentSelectedGrid called, " + \
        str(coordTuple) + " " + str(gridVal))

      pim = self.pgzIpanelMgr
      if pim is not None:
        mia = pim.matrixImgActor
        if mia is not None: 
          #mia.opacity= self.transparentImgVal
          animate(mia, opacity=self.transparentImgVal, 
               tween   =self.transparencyAnimTween,
               duration=self.transparencyAnimDuration)

    except: self.err("screenAugmentSelectedGrid"); return None

### end ###
