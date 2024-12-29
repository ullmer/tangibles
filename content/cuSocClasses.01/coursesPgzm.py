# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import sys, os, traceback
import spectra
import pygame

from pygame            import time
from enoMidiController import *
from time              import sleep #mixture of time noted, should resolve
from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesCsv        import *
from courseAssignments import *

portrait=False #mini display default-configs as portrait
if portrait: WIDTH, HEIGHT = 480, 1920
else:        WIDTH, HEIGHT = 1920, 480

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

################### coursesPg ################### 

class CoursesPgzm(CoursesPgz):
  emc              = None #enodia midi controller
  numSliders       = 9
  sliderValDict    = None
  sliderValDefault = 64
  sliderFullrange  = 128

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    self.sliderValDict = {}
    for i in range(self.numSliders): self.sliderValDict[i] = self.sliderValDefault

  ################## error ##################

  def err(self, msg): print("CoursesPgzm error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzm msg:",   msg)

  def midiCB(control, arg):   print("cpgzm midicb: ", str(control), str(arg))

  def drawSliders(self): 
    try:
      for i in range(self.numSliders)


  def drawSlider(self, whichSlider): 

  def draw(self): screen.clear(); pass
  def on_mouse_down(self, pos):   pass #cpgz.on_mouse_down(pos)
  def update(self):               self.emc.pollMidi()

def draw(): screen.clear(); cpgz.draw(screen)
def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)
def update():               cpgz.update()

################### main ################### 

emc   = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)
cpgzm = CoursesPgzm(emc=emc)

emc.registerControls(midiCB)
for i in range(64): emc.midiOut.note_on(i, i, 3)

### end ###
