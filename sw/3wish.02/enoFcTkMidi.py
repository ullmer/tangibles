# Initial weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import sys, traceback # for assisting error debugging (without code failing)

basedir = 'c:/git/tangibles/sw/3wish.02' #update to location of source if manually installed, or None otherwise

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkMidi:

  numSliders    = 9
  tkSliderWidth = 300
  tkSliderNames = None

  useTk      = True 
  useEnoMidi = True # Enodia MIDI controller class
  useMidi    = False
  useFreecad = False
  autolaunch = True  #autostart all core behaviors (including scheduled callbacks)

  swBasePath     = None

  tkActive       = None
  midiActive     = None
  freecadActive  = None

  functoolsLoaded = None  #Many (etc.) FreeCAD users may not have all 
  tkLoaded        = None  # relevant Python packages or (for MIDI)
  pilLoaded       = None  # devices installed.  This shouldn't cause
  pygameLoaded    = None  # things to break
  midiLoaded      = None  
  enoMidiLoaded   = None  
  freecadLoaded   = None  

  reportErrorAsStdout = True  # use print statement
  
  midiIn      = None  #initially singular variable; eventually multi-device
  midiOut     = None
  enoMidiCtlr = None  #hopefully will migrate to auto-identify, but not there yet
  enoMidiControllerProfile = 'aka_apcmini2'
  
  useTimerCallback = True
  useIdleCallback  = False # I view SoIdle callback as much more 
                           #  responsive to system load, but it doesn't
                           #  appear to be properly working in FreeCAD ~0.21

  idleSensor     = None
  timerSensor    = None

  tkRoot            = None
  tkWinName         = 'slider controller'
  tkSliders         = None
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
    if self.useEnoMidi: self.activateEnoMidi()
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


  ############# activate Enodia Midi controller #############

  def activateEnoMidi(self):
    try:    
      global enoMidiController
      import enoMidiController

      profile    = self.enoMidiControllerProfile 
      ourYamlDir = self.swBasePath + '/yaml'

      self.enoMidiCtlr = enoMidiController.enoMidiController(profile, 
                           yamlDir=ourYamlDir, midiCtrlOutputId=4)
      self.enoMidiLoaded = True
    except:    
      self.enoMidiLoaded = False
      self.reportError('activateMidi', 'midi import and initiation unsuccessful')
      traceback.print_exc()

  ############ update midi ############

  def updateMidi(self, arg1, arg2):
    e = self.midiIn.read(100);
    if len(e) > 2:
       events = e[1:]
       print(e)
       #print(len(events), events)
       #for event in e[1]: print("event:", event)

  def updateEnoMidi(self, arg1, arg2):
    self.enoMidiCtlr.pollMidi()

  ############ update midi ############

  def updateTk(self, arg1, arg2): self.tkRoot.update()

  ############ update all ############

  def updateAll(self, arg1, arg2):
    print(">", endline=''); sys.stdout.flush()

    if self.useTk      and self.tkLoaded   and self.tkActive:   self.updateTk(arg1, arg2)
    if self.useMidi    and self.midiLoaded and self.midiActive: self.updateMidi(arg1, arg2)
    if self.useEnoMidi and self.enoMidiLoaded:                  self.updateEnoMidi(arg1, arg2)  

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
      self.tkRoot.winfo_toplevel().title(self.tkWinName)
      self.tkActive  = True
      self.tkSliderOrient = tk.HORIZONTAL #tk.VERTICAL
    except: 
      self.tkActive = False
      self.reportError('buildTkUi', 'Initial invocation of Tkinter unsuccessful.')

    self.tkSliders    = {}

    for i in range(self.numSliders):
      f = tk.Frame(self.tkRoot)
      l = tk.Label(f, text=str(i))

      s = self.tkSliders[i] = tk.Scale(f, 
            length=self.tkSliderWidth, orient=self.tkSliderOrient, 
            from_ = self.tkSliderMinVal, to=self.tkSliderMaxVal,
            showvalue=self.tkSliderShowValue)

      l.pack(side=tk.LEFT) #textual label on left
      s.pack(side=tk.LEFT) #with slider on right
      f.pack(side=tk.TOP)  #and pack to the top

    buttonFrame = tk.Frame(self.tkRoot)

    getCb = partial(self.getTkSliderValsCb, self)
    getButton = tk.Button(buttonFrame, text='get slider vals', command=getCb)

    setCb = partial(self.setTkSliderValsCb, self)
    setButton = tk.Button(buttonFrame, text='reset slider vals', command=setCb)

    getButton.pack(side=tk.LEFT)
    setButton.pack(side=tk.LEFT)
    buttonFrame.pack(side=tk.TOP)

  ############ tk slider button callbacks ############

  def getTkSliderValsCb(self, arg): print(self.getTkSliderVals())

  def setTkSliderValsCb(self, arg):
    vals = []
    for i in range(self.numSliders): vals.append(0)
    self.setTkSliderVals(vals)

  ############ get tk slider val ############

  def getTkSliderVal(self, whichSlider):
    if whichSlider not in self.tkSliders:
      self.reportError('getTkSliderVal', 'invalid whichSlider val used'); return None

    s = self.tkSliders[whichSlider]
    result = s.get()
    return result

  ############ get tk slider vals ############

  def getTkSliderVals(self):
    result = []
    for i in range(self.numSliders):
      val = self.getTkSliderVal(i)
      result.append(val)
    
    return result

  ############ set tk slider val ############

  def setTkSliderVal(self, whichSlider, whichVal):
    if whichSlider not in self.tkSliders:
      self.reportError('setTkSliderVal', 'invalid whichSlider val used'); return None

    s = self.tkSliders[whichSlider]
    result = s.set(whichVal)

  ############ get tk slider vals ############

  def setTkSliderVals(self, vals):
    if len(vals) != self.numSliders:
      self.reportError('setTkSliderVals', 'number of vals does not equal number of sliders')
      return None

    i=0
    for val in vals: val = self.setTkSliderVal(i, val); i += 1

  ############ run autolaunch ############

  def runAutolaunch(self):
    if self.useTk: self.buildTkUi()

    if self.useFreecad and self.useIdleCallback:  self.scheduleIdleSensor()
    if self.useFreecad and self.useTimerCallback: self.scheduleTimerSensor()

#############################################################
############# freecad-free tkinter environment ##############

def tkMain():
  global basedir #base directory filename (at least originally) declared at beginning of this file
  eftm = enoFcTkMidi(useFreecad = False, useMidi = False, swBasePath=basedir)
  eftm.tkRoot.mainloop()

############################################
################### main ###################

if __name__ == '__main__':
  tkMain()

### end ###
