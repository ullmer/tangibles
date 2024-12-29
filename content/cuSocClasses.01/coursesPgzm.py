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
from coursesPgz        import *

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
  sliderFullrangeV = 128 #fullrange of sliders, relative to internal value
  sliderFullrangeP = 128 #fullrange of sliders, relative to pixels
  sliderImgFn       = 'ak_apc_mm2_s01_1920'
  sliderADict       = None #slider actor dict: one actor per sliderr 

  sliderWidth      = 180
  sliderHeight     = 10

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    self.initSliders()

  ################## error ##################

  def err(self, msg): print("CoursesPgzm error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzm msg:",   msg)

  def midiCB(self, control, arg):   print("cpgzm midicb: ", str(control), str(arg))

  ################## initSliders ##################

  def initSliders(self): 
    self.sliderValDict = {}
    self.sliderADict   = {}

    for i in range(self.numSliders): 
      self.sliderValDict[i] = self.sliderValDefault
      self.sliderADict[i]   = Actor(self.sliderImgFn)

  ################## drawSlider(s) ##################

  def drawSliders(self): 
    try:
      for i in range(self.numSliders): self.drawSlider(i)
    except: self.err("drawSliders issue")

  ################## drawSlider(s) ##################

  def drawSlider(self, whichSlider): 
    try:
      if whichSlider not in self.sliderValDict: self.err("drawSlider: index unknown: " + str(whichSlider)); return
      val     = self.sliderValDict[whichSlider]
      normVal = float(val) / float(self.sliderFullrangeV)

      x1 = self.x0 + self.dx * whichSlider
      y1 = self.y0 + int(normVal * float(self.sliderFullrangeP))

      #self.msg("drawSlider: " + str(list[whichSlider, x1, y1]))

      a = self.sliderADict[whichSlider]
      #a.topleft = (x1, y1)
      a.pos= (x1, y1)

    except: self.err("drawSlider issue with slider #" + str(whichSlider))

  ################## draw ##################

  def draw(self, screen):         super().draw(screen); self.drawSliders()
  def on_mouse_down(self, pos):   pass #cpgz.on_mouse_down(pos)
  def update(self):               self.emc.pollMidi()

################### main ################### 

emc   = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)
cpgzm = CoursesPgzm(emc=emc)

emc.registerControls(cpgzm.midiCB)

for i in range(64): emc.midiOut.note_on(i, i, 3)

def draw(): screen.clear(); cpgzm.draw(screen)
def on_mouse_down(pos):     pass #cpgzm.on_mouse_down(pos)
def update():               cpgzm.update()

### end ###
