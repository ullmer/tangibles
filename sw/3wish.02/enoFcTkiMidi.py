# Initial weaving of weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import sys

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkiMidi:
  numSliders     = 8
  tkiSliderWidth = 300
  tkiSliderNames = None

  useTki     = True 
  useMidi    = True
  useFreecad = True
  autolaunch = True  #autostart all core behaviors (including scheduled callbacks)

  tkiActive      = None
  midiActive     = None
  freecadActive  = None

  functoolsLoaded = None  #Many (etc.) FreeCAD users may not have all 
  tkiLoaded       = None  # relevant Python packages or (for MIDI)
  pilLoaded       = None  # devices installed.  This shouldn't cause
  pygameLoaded    = None  # things to break
  midiLoaded      = None  
  freecadLoaded   = None  

  reportErrorAsStdout = True  # use print statement
  
  midiIn  = None  #initially singular variable; eventually multi-device
  midiOut = None
  
  useTimerCallback = True
  useIdleCallback  = False # I view SoIdle callback as much more 
                           #  responsive to system load, but it doesn't
                           #  appear to be properly working in FreeCAD ~0.21

  idleSensor      = None
  timerSensor     = None

  tkiRoot         = None
  tkiSliders      = None
  tkiSliderVals   = None

  tkiSliderMinVal = 0
  tkiSliderMaxVal = 10

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useFreecad: self.activateFreecad() 
    if self.useTki:     self.activateTki();     self.buildTkiUi()
    if self.useMidi:    self.activateMidi();    self.buildMidi()
    if self.autolaunch: self.runAutolaunch() #naming of these two may benefit from revisiting

  ############# report error#############

  def reportError(self, methodCalled, errorMsg): #with an eye toward VR, etc.
    if self.reportErrorAsStdout:
      print("error: enoFcTkiMidi %s: %s" % (methodCalled, errorMsg))

  ############# activate Freecad #############

  def activateFreecad(self):
    try:    
      import FreeCAD as App
      import FreeCADGui as Gui
      import pivy.coin as coin
      self.freecadLoaded = True
    except:    
      self.freecadLoaded = False
      self.reportError('activateFreecad', 'FreeCAD imports unsuccessful.')

    #from w3core  import *
    #from w3shift import *

  ############# activate Tkinter #############

  def activateTki(self):
    try:    
      global tkinter #sad, but this appears ~necessary with this loading approach
      import tkinter 
      self.tkiLoaded = True #let's initially assume that successful import 
                             #indicates "working." Later with embedded devices
			     #in particular, this may wish to become more nuanced.
    except: 
      self.tkiLoaded = False
      self.reportError('activateTki', 'tkinter import unsuccessful.')

    try: 
      global partial
      from functools import partial
      self.functoolsLoaded = True
    except: 
      self.functoolsLoaded = False
      self.reportError('activateTki', 'functools import (for callback "partials") unsuccessful.')

    try: 
      self.tkiRoot   = tkinter.Tk() # Create the root (base) window
      self.tkiActive = True
    except: 
      self.tkiActive = False
      self.reportError('activateTki', 'Initial invocation of Tkinter unsuccessful.')

    #later: import PIL.Image, PIL.ImageTk #image manipulation package

  ############# activate Midi #############

  def activateMidi(self):
    try:    
      global pg
      import pygame as pg
      self.pygameLoaded = True
    except:    
      self.pygameLoaded = False
      self.reportError('activateMidi', 'pygame import unsuccessful')

    try:    
      global pygame
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
    if self.timerSensor is None:  #avoid relaunch
       self.timerSensor = coin.SoTimerSensor(self.updateAll, 0) 
       self.timerSensor.schedule()  # by default, appears ~30 updates per second

  ############ schedule Idle Sensor updates ############

  def scheduleIdleSensorUpdates(self):
    self.reportError('scheduleIdleSensorUpdates', 
       "Ullmer views SoIdle callback as much more responsive to system load,\n" +
       "but SoIdle doesn't appear to be properly working in FreeCAD ~0.21.\n" +
       "Launching TimerSensor as alternative")

    self.scheduleTimerSensorUpdates() #unsure of this choice, but initially...

  ############ build tkinter user interface ############

  def buildTkiUi(self):
    self.tkiSliders    = {}
    self.tkiSliderVals = {}

    for i in range(self.numSliders):
      self.tkiSliderVals[i] = 0
      s = self.tkiSliders[i] = tkinter.Scale(self.tkiRoot, variable=self.tkiSliderVals[i], \
            length=self.tkiSliderWidth, \
            from_ = self.tkiSliderMinVal, to=self.tkiSliderMaxVal)
      s.pack(side=tkinter.TOP)

    #tkiSliderNames = None

  ############ run autolaunch ############

  def runAutolaunch(self):
    if self.useTki: self.buildTkiUi()

    if self.useFreecad and self.useIdleCallback:  self.scheduleIdleSensor()
    if self.useFreecad and self.useTimerCallback: self.scheduleTimerSensor()

#############################################################
############# freecad-free tkinter environment ##############

def tkiMain():
  eftm = enoFcTkiMidi(useFreecad = False, useMidi = False)
  eftm.tkiRoot.mainloop()

############################################
################### main ###################

if __name__ == '__main__':
  tkiMain()

### end ###
