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

################### coursesPg ################### 

class CoursesPgzm(CoursesPgz):
  emc              = None #enodia midi controller
  numSliders       = 9
  sdx0, sdx        = 1, 1.3 #differences in slider x0, dx relative to CoursesPgz
  sliderValDict    = None
  sliderValDefault = 128 
  sliderFullrangeV = 128 #fullrange of sliders, relative to internal value
  sliderFullrangeP = 338#fullrange of sliders, relative to pixels
  sliderImgFn      = 'ak_apc_mm2_s01_1920'
  sliderADict      = None #slider actor dict: one actor per sliderr 
  verbose          = False

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    self.initSliders()

  ################## error ##################

  def err(self, msg): print("CoursesPgzm error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzm msg:",   msg)

  ################## midi callback ##################

  def midiCB(self, control, arg):   
    try:
      if self.verbose: print("cpgzm midicb: ", str(control), str(arg))
      whichSlider = int(control[-1]) - 1 #control is "s1", "s2", etc.
      whichVal    = int(arg)
      self.sliderValDict[whichSlider] = self.sliderFullrangeV - whichVal
    except: self.err("midiCb " + str([control, arg]))

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

      x = self.x0 + self.sdx0 + ((self.dx + self.sdx) * whichSlider)
      y = self.y0 + int(normVal * float(self.sliderFullrangeP))

      #self.msg("drawSlider: " + str(list[whichSlider, x1, y1]))

      a = self.sliderADict[whichSlider]
      a.topleft = (x, y)
      a.draw()

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
