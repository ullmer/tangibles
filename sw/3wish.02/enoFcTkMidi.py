# Initial weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import sys, traceback # for assisting error debugging (without code failing)

from time import sleep
from functools import partial

basedir = 'c:/git/tangibles/sw/3wish.02' #update to location of source if manually installed, or None otherwise

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkMidi:

  numSliders    = 9
  tkSliderWidth = 150
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

  freecadHoldsMainloop = False
  tkHoldsMainloop      = True

  tkLoaded        = None  #Many (etc.) FreeCAD users may not have all 
  pilLoaded       = None  # relevant Python packages or (for MIDI)
  pygameLoaded    = None  # devices installed.  This shouldn't cause
  midiLoaded      = None  # things to break
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

  showButtonGrid2D  = True
  showSliders2D     = True

  tkRoot            = None
  tkWinName         = 'slider controller'
  tkSliders         = None
  tkSliderOrient    = 'vert' # or 'horiz'
  tkSliderShowValue = 0
  tkSliderLength    = 17
  tkBgRgb           = [10]  * 3
  tkFgRgb           = [170] * 3

  #tkSliderMinVal = 0
  #tkSliderMaxVal = 127

  tkSliderMinVal = 127
  tkSliderMaxVal = 0

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useFreecad: self.activateFreecad() 
    if self.useTk:      self.activateTk();     self.buildTkUi()
    if self.useMidi:    self.activateMidi();   self.buildMidi()
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
    if not self.tkHoldsMainloop and self.useTk and self.tkLoaded   and self.tkActive:   
      self.updateTk(arg1, arg2) #if tk holds mainloop, it will manage Tk updates

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
    except: 
      self.tkActive = False
      self.reportError('buildTkUi', 'Initial invocation of Tkinter unsuccessful.')

    r,g,b = self.tkBgRgb
    bgCol = self.rgb2tk(r,g,b)

    sliderFrame = tk.Frame(self.tkRoot, bg=bgCol)
    bGridFrame  = tk.Frame(self.tkRoot, bg=bgCol)

    if self.showSliders2D:    self.buildSliders(sliderFrame)
    if self.showButtonGrid2D: self.buildButtonGrid(bGridFrame)

    for el in [sliderFrame, bGridFrame]: el.pack(side=tk.LEFT)

  ############ build button grid user interface ############

  def buildButtonGrid(self, rootFrame):
    self.reportError('buildButtonGrid', 'not yet implemented')

  #https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
  #translates rgb values of type int to a tkinter friendly color code

  ############ build sliders user interface ############

  def rgb2tk(self, r, g, b):
    return "#%02x%02x%02x" % (r,g,b)

  ############ build sliders user interface ############

  def buildSliders(self, rootFrame):
    r,g,b = self.tkBgRgb
    bgCol = self.rgb2tk(r,g,b)
    rootFrame.bg = bgCol

    r,g,b = self.tkFgRgb
    fgCol = self.rgb2tk(r,g,b)

    self.tkSliders    = {}

    for i in range(self.numSliders):
      
      f = tk.Frame(rootFrame, bg=bgCol)
      l = tk.Label(f, text=str(i), bg=bgCol, fg=fgCol)

      if self.tkSliderOrient == 'vert': sOrient = tk.VERTICAL
      else:                             sOrient = tk.HORIZONTAL

      s = self.tkSliders[i] = tk.Scale(f, bg=bgCol,
            length = self.tkSliderWidth,  orient       = sOrient,
            from_  = self.tkSliderMinVal, showvalue    = self.tkSliderShowValue, 
            to     = self.tkSliderMaxVal, sliderlength = self.tkSliderLength)

      if self.tkSliderOrient == 'vert':
        l.pack(side=tk.BOTTOM) #textual label on left
        s.pack(side=tk.BOTTOM) #with slider on right
        f.pack(side=tk.LEFT)  #and pack to the top
      else:
        l.pack(side=tk.LEFT) #textual label on left
        s.pack(side=tk.LEFT) #with slider on right
        f.pack(side=tk.TOP)  #and pack to the top

    buttonFrame = tk.Frame(rootFrame)

    getCb = partial(self.getTkSliderValsCb, self)
    getButton = tk.Button(buttonFrame, text='get slider vals', command=getCb)

    setCb = partial(self.setTkSliderValsCb, self)
    setButton = tk.Button(buttonFrame, text='reset slider vals', command=setCb)

    if self.tkSliderOrient == 'vert':
      getButton.pack(side=tk.TOP)
      setButton.pack(side=tk.TOP)
      buttonFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
    else:
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

  ############ midi event callback############

  def midiEventCb(self, control, arg):
    try:
      ctrlType = control[0]
      ctrlId   = int(control[1])
      ctrlVal  = int(arg)
 
      if ctrlType == 's': 
        #print(ctrlId, ctrlVal)
        self.setTkSliderVal(ctrlId-1, ctrlVal)
 
    except:
      reportError(self, 'midiEventCb', "error parsing midi event information")

##############################################
############# update midi, etc. ##############

def afterIdleCb(eftm): 
  eftm.updateAll(0,0)
  tkUpdate = partial(afterIdleCb, eftm)
  tkUpdate.__name__ = 'ourTkUpdate' # This is necessary because of a ~bug on line ~821 of tkinter __init__

  eftm.tkRoot.update()
  eftm.tkRoot.after(50, tkUpdate)

############# freecad-free tkinter environment ##############

def tkMain():
  global basedir, afterIdleCb

  eftm = enoFcTkMidi(useFreecad = False, useMidi = False, swBasePath=basedir)

  tkUpdate = partial(afterIdleCb, eftm)
  tkUpdate.__name__ = 'ourTkUpdate' # This is necessary because of a ~bug on line ~821 of tkinter __init__
  eftm.tkRoot.after(50, tkUpdate)

  emc = eftm.enoMidiCtlr
  #emc.registerControls(emc.debugCallback)
  emc.registerControls(eftm.midiEventCb)

  eftm.tkRoot.mainloop()

############################################
################### main ###################

if __name__ == '__main__':
  tkMain()

### end ###
