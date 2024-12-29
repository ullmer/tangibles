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
  emc = None #enodia midi controller

  def midiCB(control, arg):   print("midicb: ", str(control), str(arg))
  def draw(): screen.clear(); pass
  def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)
  def update():               emc.pollMidi()

def draw(): screen.clear(); cpgz.draw(screen)
def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)
def update():               cpgz.update()

################### main ################### 

emc = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)
cpgzm = CoursesPgzm(emc=emc)

emc.registerControls(midiCB)
for i in range(64): emc.midiOut.note_on(i, i, 3)

### end ###
