# Initial weaving of weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import sys

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkMidi:
  numSliders    = 8
  tkSliderWidth = 300
  tkSliderNames = None

  useTk      = True 
  useMidi    = True
  useFreecad = True
  autolaunch = True  #autostart all core behaviors (including scheduled callbacks)

  tkActive       = None
  midiActive     = None
  freecadActive  = None

  functoolsLoaded = None  #Many (etc.) FreeCAD users may not have all 
  tkLoaded        = None  # relevant Python packages or (for MIDI)
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

  idleSensor     = None
  timerSensor    = None

  tkRoot            = None
  tkSliders         = None
  tkSliderVals      = None
  tkSliderOrient    = None
  tkSliderShowValue = 0

  tkSliderMinVal = 0
  tkSliderMaxVal = 10

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useFreecad: self.activateFreecad() 
    if self.useTk:      self.activateTk();     self.buildTkUi()
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

  def activateTk(self):
    try:    
      global tk #sad, but this appears ~necessary with this loading approach
      import tkinter as tk 
      self.tkLoaded = True #let's initially assume that successful import 
                           #indicates "working." Later with embedded devices
                           #in particular, this may wish to become more nuanced.
    except: 
      self.tkLoaded = False
      self.reportError('activateTk', 'tk import unsuccessful.')

    try: 
      global partial
      from functools import partial
      self.functoolsLoaded = True
    except: 
      self.functoolsLoaded = False
      self.reportError('activateTk', 'functools import (for callback "partials") unsuccessful.')

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

  def updateTk(self, arg1, arg2): self.tkRoot.update()

  ############ update all ############

  def updateAll(self, arg1, arg2):
    if self.useTk  and self.tkLoaded  and self.tkActive:  self.updateTk(arg1, arg2)
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

  ############ build tk user interface ############

  def buildTkUi(self):
    if self.tkRoot is not None: return # don't rebuild multiple times

    try: 
      self.tkRoot    = tk.Tk() # Create the root (base) window
      self.tkActive  = True
      self.tkSliderOrient = tk.HORIZONTAL #tk.VERTICAL
    except: 
      self.tkActive = False
      self.reportError('buildTkUi', 'Initial invocation of Tkinter unsuccessful.')

    self.tkSliders    = {}
    self.tkSliderVals = {}

    for i in range(self.numSliders):
      self.tkSliderVals[i] = 0

      f = tk.Frame(self.tkRoot)
      l = tk.Label(f, text=str(i))

      s = self.tkSliders[i] = tk.Scale(f, variable=self.tkSliderVals[i], 
            length=self.tkSliderWidth, orient=self.tkSliderOrient, 
            from_ = self.tkSliderMinVal, to=self.tkSliderMaxVal,
            showvalue=self.tkSliderShowValue)

      l.pack(side=tk.LEFT) #textual label on left
      s.pack(side=tk.LEFT) #with slider on right
      f.pack(side=tk.TOP)  #and pack to the top

    #tkiSliderNames = None

  ############ run autolaunch ############

  def runAutolaunch(self):
    if self.useTk: self.buildTkUi()

    if self.useFreecad and self.useIdleCallback:  self.scheduleIdleSensor()
    if self.useFreecad and self.useTimerCallback: self.scheduleTimerSensor()

#############################################################
############# freecad-free tkinter environment ##############

def tkMain():
  eftm = enoFcTkMidi(useFreecad = False, useMidi = False)
  eftm.tkRoot.mainloop()

############################################
################### main ###################

if __name__ == '__main__':
  tkMain()

### end ###
