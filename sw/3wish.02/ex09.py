# First validation of Python port of 1995 3wish code
# Brygg Ullmer, Clemson University
# Original code begun fall 1995; here, 2023-10-20

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import sys
import pygame as pg
import pygame.midi

basedir = 'c:/git/tangibles/sw/3wish.02'
sys.path.append(basedir)
from w3core     import *
from enoFreecad import *

view, doc, sg, root = genViewDocSgRoot()

yamlFn = basedir + '/scene01.yaml'
efc    = enoFreecad(yamlFn, doc)

bldgCut1   = App.activeDocument().addObject("Part::Cut", "Bldg central void")
bldgCut1.Base = efc.getObj("bldg1a")
bldgCut1.Tool = efc.getObj("bldg1b")

doc.recompute()

setCameraconfig(efc.getCameraConfig("cam1"))

pygame.midi.init()

############ update midi ############

def updateMidi(arg1, arg2):
  global midiIn
  e = midiIn.read(100); 
  if len(e) > 2: 
     events = e[1:]
     #print(e)
     print(len(events), events)
     #for event in e[1]

global midiIn
midiIn = pygame.midi.Input(1)

e = midiIn.read(100); print(e)

ts = coin.SoTimerSensor(updateMidi, 0)
ts.schedule()

### end ###
