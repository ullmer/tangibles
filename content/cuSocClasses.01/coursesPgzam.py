# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import sys, os, traceback
import spectra
import pygame

from pygame              import time
from enoMidiController   import *
from time                import sleep #mixture of time noted, should resolve
from pgzero.builtins     import Actor, animate, keyboard, keys
from coursesPgzAccordion import *

################### coursesPgz Accordion + MIDI ################### 

class CoursesPgzam(CoursesPgzAccordion):
  emc              = None #enodia midi controller
  numSliders       = 9
  sdx0, sdx        = 1, 1.3 #differences in slider x0, dx relative to CoursesPgz
  sliderValDict    = None
  sliderValDefault = 128 
  sliderFullrangeV = 128 #fullrange of sliders, relative to internal value
  sliderFullrangeP = 338 #fullrange of sliders, relative to pixels
  sliderImgFn      = 'ak_apc_mm2_s01_1920'
  sliderADict      = None #slider actor dict: one actor per sliderr 
  verbose          = False
  mColColorIndices  = [45, 5, 25, 9]
  mColorBrights     = [1, 6, 10]

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

      if control[0] == 's': #slider
        whichSlider = int(control[-1]) - 1 #control is "s1", "s2", etc.
        whichVal    = int(arg)
        mappedVal   = self.mapSliderVal(whichSlider, whichVal)

        self.sliderValDict[whichSlider] = self.sliderFullrangeV - whichVal
        #self.sliderValDict[whichSlider] = mappedVal
        self.assignColumnIdx(whichSlider, mappedVal)

    except: self.err("midiCb " + str([control, arg]))

  ################## initSliders ##################

  def mapSliderVal(self, whichCol, whichSliderVal): 
    try:
      colLen = self.getColLenByIdx(whichCol)
      result = int((1.-float(whichSliderVal)/float(self.sliderFullrangeV)) * colLen)
      return result

    except: self.err("mapSliderVal issue:")
     
  ################## initSliders ##################

  def initSliders(self): 
    self.sliderValDict   = {}
    self.sliderADict     = {}

    for i in range(self.numSliders): 
      self.sliderValDict[i]   = self.sliderValDefault
      self.sliderADict[i]     = Actor(self.sliderImgFn)

  ################## drawSlider(s) ##################

  def drawSliders(self): 
    try:
      for i in range(self.numSliders): self.drawSlider(i)
    except: self.err("drawSliders issue")

  ################## set akai color index coordinate ##################

  def setAkaiColorIdxCoord(self, colorIdx, x, y, colorBright=6): #(0,0) = bottom-left = MIDI note 0
    coord   = self.mapAkaiCoord(x, y)
    mcciLen = len(self.mColColorIndices)
    if colorIdx < 0 or colorIdx >= mcciLen: self.msg("setAkaiColorIdxCoord issue with colorIdx " + str(colorIdx)); return

    colorVal = self.mColColorIndices[colorIdx]
    self.emc.midiOut.note_on(coord, colorVal, colorBright)

  ################## mapAkaiCoord ##################

  def mapAkaiCoord(self, x, y): #(0,0) = bottom-left = MIDI note 0
    result = x + (y*8)
    return result

  ################## update matrix colors ##################

  def updateMatrixColors(self): 

    for colIdx in range(8):
      for row  in range(8):
        pass #self.setAkaiColorIdxCoord()

        #cpgzam.setAkaiColorIdxCoord(j, j+4, i, 1)

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
cpgzam = CoursesPgzam(emc=emc)

emc.registerControls(cpgzam.midiCB)

#for i in range(6): emc.midiOut.note_on(i, i, 3)
#for i in range(64): emc.midiOut.note_on(i, i, 3)
#blue 45 orange 5 green 25 brown 9

#for i in [45, 5, 25, 9]:  emc.midiOut.note_on(i, i,   1)
#for i in [46, 6, 26, 10]: emc.midiOut.note_on(i, i-1, 6)
#for i in [47, 7, 27, 11]: emc.midiOut.note_on(i, i-2, 10)

#for i in range(9):
#  for j in range(4):
#     cpgzam.setAkaiColorIdxCoord(j, j+4, i, 1)
  
def draw(): screen.clear(); cpgzam.draw(screen)
def on_mouse_down(pos):     pass #cpgzm.on_mouse_down(pos)
def update():               cpgzam.update()

### end ###
