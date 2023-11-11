# Initial weaving of weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import sys

from w3core  import *
from w3shift import *

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkiMidi:
  numSliders     = 8
  tkiSliderWidth = 300
  tkiSliderNames = None

  useTki     = True 
  useMidi    = True
  autolaunch = True  #autostart all core behaviors (including scheduled callbacks)

  tkiActive  = None
  midiActive = None

  functoolsLoaded = None  #Many (etc.) FreeCAD users may not have all 
  tkiLoaded       = None  # relevant Python packages or (for MIDI)
  pilLoaded       = None  # devices installed.  This shouldn't cause
  pygameLoaded    = None  # things to break
  midiLoaded      = None  
  
  midiIn  = None  #initially singular variable; eventually multi-device
  midiOut = None
  
  useTimerCallback = True
  useIdleCallback  = False # I view SoIdle callback as much more 
                           #  responsive to system load, but it doesn't
                           #  appear to be properly working in FreeCAD ~0.21

  timerSensor = None
  tkiRoot     = None

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useTki:     self.activateTki();  self.buildTki()
    if self.useMidi:    self.activateMidi(); self.buildMidi()
    if self.autolaunch: self.runAutolaunch() #naming of these two may benefit from revisiting

  ############# activate Tkinter #############

  def activateTki(self):
    try:    
      from tkinter   import *
      self.tkiLoaded = True #let's initially assume that successful import 
                             #indicates "working." Later with embedded devices
			     #in particular, this may wish to become more nuanced.
    except: 
      self.tkiLoaded = False
      self.reportError('activateTki', 'tkinter import unsuccessful.')

    try: 
      from functools import partial
      self.functoolsLoaded = True
    else: 
      self.functoolsLoaded = False
      self.reportError('activateTki', 'functools import (for callback "partials") unsuccessful.')

    try: 
      self.tkiRoot   = Tk() # Create the root (base) window
      self.tkiActive = True
    except: 
      self.tkiActive = False
      self.reportError('activateTki', 'Initial invocation of Tkinter unsuccessful.')

    #later: import PIL.Image, PIL.ImageTk #image manipulation package

  ############# activate Midi #############

  def activateMidi(self):
    try:    
      import pygame as pg
      self.pygameLoaded = True
    except:    
      self.pygameLoaded = False
      self.reportError('activateMidi', 'pygame import unsuccessful')

    try:    
      import pygame.midi
      pygame.midi.init()
      self.midiLoaded = True
      self.midiIn = pygame.midi.Input(1) #initially hardcoded
    except:    
      self.midiLoaded = False
      self.reportError('activateMidi', 'midi import and initiation unsuccessful')

  ############ update midi ############

  def updateMidi(self, arg1, arg2):
    e = self.midiIn.read(100);
    if len(e) > 2:
       events = e[1:]
       print(e)
       #print(len(events), events)
       #for event in e[1]: print("event:", event)

  ############ update midi ############

  def updateTki(self, arg1, arg2): self.tkiRoot.update()

  ############ update all ############

  def updateAll(self, arg1, arg2):
    if self.useTki  and self.tkiLoaded  and self.tkiActive:  self.updateTki(arg1, arg2)
    if self.useMidi and self.midiLoaded and self.midiActive: self.updateMidi(arg1, arg2)

  ############ schedule Timer Sensor updates ############

  def scheduleTimerSensorUpdates(self):
    self.timerSensor = coin.SoTimerSensor(self.updateAll, 0) 
    self.timerSensor.schedule()  # by default, appears ~30 updates per second

### end ###
