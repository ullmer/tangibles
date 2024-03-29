# Initial weaving of FreeCAD and kin, Tkinter, and midi controls
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import sys, traceback # for assisting error debugging (without code failing)
import PySide

from time import sleep
from functools import partial
from PySide import QtCore, QtGui

basedir = 'c:/git/tangibles/sw/3wish.02' #update to location of source if manually installed, or None otherwise

################### Enodia FreeCAD Tkinter Midi controls ###################

class enoFcTkMidi:

  numSliders    = 9
  tkSliderWidth = 75
  tkSliderNames = None

  useTk      = True 
  useEnoMidi = False # Enodia MIDI controller class
  useMidi    = False
  useFreecad = False
  autolaunch = True  #autostart all core behaviors (including scheduled callbacks)
  updateTkTitlebar = False

  swBasePath     = None
  swIconFn       = '/images/enodiaTkTitlebar01g.png'

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
  
  midiIn       = None  #initially singular variable; eventually multi-device
  midiOut      = None
  enoMidiCtlr  = None  #hopefully will migrate to auto-identify, but not there yet
  enoMidiControllerProfile = 'aka_apcmini2'

  etkColorGrid = None
  
  useTimerCallback = False
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
  tkSTroughRgb      = [130] * 3 #slider trough
  tkFgRgb           = [170] * 3
  tkButBgRgb        = [50]  * 3 #background near buttons

  qtSliderTab       = None
  qPalette          = None
  bgHlColor         = "#ff0050"
  qtSliders         = None
  numSliders        = 9
  sliderBase        = [-16., -276., 15.3]
  sliderRanges      = [100., 10., 1.]

  sliderOffsets     = None
  qtHeaderLabel     = None
  qtHeaderLabelTxt1 = \
           "  x             y             z        \n" + \
           "  10  1  .1     10  1  .1     10  1  .1\n" 

  qtHeaderLabelTxt2 = \
           "  x: -0.02      y: 0.015      z: 0.3"

  qtHeaderLabelTxt  = None
  fcActiveTranslationNode = None

  #tkSliderMinVal = 0
  #tkSliderMaxVal = 127

  tkSliderMinVal = 127
  tkSliderMaxVal = 0
  lightState     = 0

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useFreecad: self.activateFreecad() ; self.buildFCUi()
    if self.useTk:      self.activateTk();     self.buildTkUi()
    if self.useMidi:    self.activateMidi();   self.buildMidi()
    if self.useEnoMidi: self.activateEnoMidi()
    if self.autolaunch: self.runAutolaunch() #naming of these two may benefit from revisiting

  ############# report error #############

  def reportError(self, methodCalled, errorMsg): #with an eye toward VR, etc.
    if self.reportErrorAsStdout:
      print("error: enoFcTkiMidi %s: %s" % (methodCalled, errorMsg))

#https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Code_snippets.md#add-a-tab-to-the-combo-view

  ############# get main window #############

  def getMainWindow(self):
    "returns the main window"
    # using QtGui.qApp.activeWindow() isn't very reliable because if another
    # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
    # returned

    #toplevel = QtGui.qApp.topLevelWidgets()
    toplevel = QtGui.QApplication.topLevelWidgets()
    for i in toplevel:
      if i.metaObject().className() == "Gui::MainWindow": return i
    raise Exception("No main window found")
  
  ############# get combo view #############

  def getComboView(self, mw):
    dw=mw.findChildren(QtGui.QDockWidget)
    for i in dw:
      if str(i.objectName()) == "Combo View":
        return i.findChild(QtGui.QTabWidget)
      elif str(i.objectName()) == "Python Console":
        return i.findChild(QtGui.QTabWidget)
    raise Exception ("No tab widget found")

  ############# slider update callback #############

# IMPORTANT NOTE: unless FreeCad -> Preferences -> Python -> 
#   Macro -> Run macros in local environment is unchecked, Qt callbacks
#   do not appear to work, nor are script objects accessible from the terminal.

  def sliderUpdate(self, sliderNum, value):
    v = self.calcSliderInflectedXYZ()
    self.updateSliderText(v)

    if self.fcActiveTranslationNode is not None:
      tv = self.fcActiveTranslationNode.translation.getValue()
      for i in range(3):
        tv[i] = v[i]
      self.fcActiveTranslationNode.touch() #propagate updates

    #print('slider update', sliderNum, value, v)

  ############# float to n characters #############

  def float2nchar(self, axis, val, nchars):
    result = "%s: %2.6f" % (axis, val) 
    lr = len(result)

    if lr == nchars: return result
    result = str(result)

    if lr   > nchars: return result[0:nchars]
    diff    = lr-nchars
    result += " " * (diff+1)
    return result

  ############# updateSliderText #############

  def updateSliderText(self, xyz):
    x,y,z = xyz

    self.qtHeaderLabelTxt2  = "  "     + self.float2nchar('x', x, 8)
    self.qtHeaderLabelTxt2 += "      " + self.float2nchar('y', y, 8)
    self.qtHeaderLabelTxt2 += "      " + self.float2nchar('z', z, 8)

    self.qtHeaderLabelTxt  = self.qtHeaderLabelTxt1 + \
                             self.qtHeaderLabelTxt2
    self.qtHeaderLabel.setText(self.qtHeaderLabelTxt)

  ############# calculate slider-inflected XYZ #############
  # migrate soon to another class

  def calcSliderInflectedXYZ(self):
    result0 = []
    sb     = self.sliderBase   # e.g., [-.02, .015, .3]
    componentResult = 0

    for i in range(self.numSliders):
      sr = self.sliderRanges[i%3] # e.g., [10., 1., .1]
      sliderMod = i % 3
      if i > 0 and sliderMod == 0:
        result0.append(componentResult); componentResult = 0

      sliderVal        = self.qtSliders[i].value()/100. * sr
      componentResult += sliderVal
    result0.append(componentResult)

    sb = self.sliderBase        #[-.02, .015, .3]
    result = []

    for i in range(3):
      v = sb[i] + result0[i]
      result.append(v)

    return result

  ############# build freecad user interface #############

  def buildFCUi(self):

    mw  = self.getMainWindow()
    tab = self.getComboView(mw)
    print("build fcui2")

    self.qtHeaderLabelTxt  = self.qtHeaderLabelTxt1 + \
                             self.qtHeaderLabelTxt2

    try: tab.removeTab(2) #temp. hardcoded; prevents repeated additions
    except: print("*attempted to remove Sliders tab, failed")

    qst = QtGui.QDialog()
    self.qtSliderTab = qst
    tab.addTab(qst, "Sliders")
    self.qtSliders       = []

    slW, slH, x0, y0, dx = 14, 250, 13, 30, 31
    ldx, ldy, groupNudge = 5, 15, 16

    for i in range(self.numSliders):

     sl = QtGui.QSlider(qst)
     sl.setObjectName("a")
     geom = QtCore.QRect(x0, y0, slW, slH)
     #sl.setTickPosition(QtGui.QSlider.TickPosition.TicksLeft)
     sl.setTickPosition(sl.TicksLeft)
     sl.setTickInterval(8)
     sl.setGeometry(geom)

     sl.setRange(-100, 100)
     sl.setValue(0)
     sl.setSingleStep(10)
     sl.setPageStep(20)

     self.qtSliders.append(sl)
     sl.show()

     cb = partial(self.sliderUpdate, i)
     sl.valueChanged[int].connect(cb)

     x0 += dx
     if i%3==2: x0 += groupNudge

    qst.show()
    try: tab.setCurrentIndex(2) 
    except: print("tried to set tab 2/Sliders visible, but failed")

    f = QtGui.QFont("monospace") 
    f.setStyleHint(QtGui.QFont.Monospace);

    txt = self.qtHeaderLabelTxt
    lb = QtGui.QLabel(txt, qst)
    lb.setFont(f)
    lb.show()
    self.qtHeaderLabel = lb
    self.sliderUpdate(0, 0) #temporary hack to update translations

    #self.qtSliderLayouts = {}

    #for i in range(self.qtSliderNumFrames): #e.g., 3
    #   f = QtGui.QFrame()
    #   f.setFrameShape( QtGui.QFrame.StyledPanel)
    #   f.setFrameShadow(QtGui.QFrame.Plain)
    #   f.setLineWidth(3)
    #   lay = QtGui.QVBoxLayout(f)
    #   qst.addWidget(lay)
    #   self.qtSliderLayouts[i] = lay

#https://forum.freecad.org/viewtopic.php?t=11243
#https://www.pythontutorial.net/pyqt/pyqt-qslider/
#https://stackoverflow.com/questions/62028393/using-qframes-in-qt-for-python
#https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget
#https://srinikom.github.io/pyside-docs/PySide/QtGui/QLabel.html
#https://forum.qt.io/topic/35999/solved-qplaintextedit-how-to-change-the-font-to-be-monospaced/4

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

      #i = self.enoMidiCtlr.midiCtrlInputId
      #o = self.enoMidiCtlr.midiCtrlOutputId
      #print("input channel: %s, output channel: %s" % (i, o))

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
      if self.updateTkTitlebar: self.tkRoot.winfo_toplevel().title(self.tkWinName)
      self.tkActive  = True
    except: 
      self.tkActive = False
      self.reportError('buildTkUi', 'Initial invocation of Tkinter unsuccessful.')

    if self.updateTkTitlebar:
      try:
        iconFn = self.swBasePath + self.swIconFn
        iconPh = tk.PhotoImage(file = iconFn)
        self.tkRoot.iconphoto(False, iconPh)
      except: 
        self.reportError('buildTkUi', 'issues registering titlebar icon image; details:')
        traceback.print_exc()

    r,g,b = self.tkBgRgb
    bgCol = self.rgb2tk(r,g,b)

    sliderFrame = tk.Frame(self.tkRoot, bg=bgCol)
    bGridFrame  = tk.Frame(self.tkRoot, bg=bgCol)

    if self.showSliders2D:    self.buildSliders(sliderFrame)
    if self.showButtonGrid2D: self.buildButtonGrid(bGridFrame)

    for el in [bGridFrame, sliderFrame]: el.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

  ############ build sliders user interface ############

  def rgb2tk(self, r, g, b):
    return "#%02x%02x%02x" % (r,g,b)

  ############ build button grid user interface ############

  def buildButtonGrid(self, rootFrame):

    print("building button grid")
    try:
      global enoTkColorGrid
      import enoTkColorGrid

      self.etkColorGrid = enoTkColorGrid.enoTkColorGrid(rootFrame)

    except:
      self.reportError('buildButtonGrid', 'error:')
      traceback.print_exc()

  #https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
  #translates rgb values of type int to a tkinter friendly color code

  ############ build sliders user interface ############

  def buildSliders(self, rootFrame):
    r,g,b = self.tkBgRgb
    bgCol = self.rgb2tk(r,g,b)
    rootFrame.bg = bgCol

    r,g,b = self.tkFgRgb
    fgCol = self.rgb2tk(r,g,b)

    r,g,b = self.tkSTroughRgb
    trCol = self.rgb2tk(r,g,b)
  
    r,g,b  = self.tkButBgRgb
    bbgCol = self.rgb2tk(r,g,b)

    self.tkSliders    = {}

    for i in range(self.numSliders):
      
      f = tk.Frame(rootFrame, bg=bgCol)
      l = tk.Label(f, text=str(i), bg=bgCol, fg=fgCol)

      if self.tkSliderOrient == 'vert': sOrient = tk.VERTICAL
      else:                             sOrient = tk.HORIZONTAL

      s = self.tkSliders[i] = tk.Scale(f, bg=bgCol, relief= tk.FLAT,
            length = self.tkSliderWidth,  orient          = sOrient,
            from_  = self.tkSliderMinVal, showvalue       = self.tkSliderShowValue, 
            to     = self.tkSliderMaxVal, sliderlength    = self.tkSliderLength,
            troughcolor = trCol)

      if self.tkSliderOrient == 'vert':
        l.pack(side=tk.BOTTOM) #textual label on left
        s.pack(side=tk.BOTTOM) #with slider on right
        f.pack(side=tk.LEFT)  #and pack to the top
      else:
        l.pack(side=tk.LEFT) #textual label on left
        s.pack(side=tk.LEFT) #with slider on right
        f.pack(side=tk.TOP)  #and pack to the top

    buttonFrame = tk.Frame(rootFrame, bg=bbgCol)

    getCb = partial(self.getTkSliderValsCb, self)
    getButton = tk.Button(buttonFrame, text='get\nvals',  
                          justify=tk.RIGHT, command=getCb)

    setCb = partial(self.setTkSliderValsCb, self)
    setButton = tk.Button(buttonFrame, text='reset\nvals', 
                          justify=tk.RIGHT, command=setCb)

    lightButton = tk.Button(buttonFrame, text='light',
                            justify=tk.RIGHT, command=self.midiIlluminate)

    if self.tkSliderOrient == 'vert':
      for el in [getButton, setButton, lightButton]: el.pack(side=tk.TOP, fill=tk.X)
      buttonFrame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
    else:
      getButton.pack(side=tk.LEFT)
      setButton.pack(side=tk.LEFT)
      buttonFrame.pack(side=tk.TOP)

  ############ midiIlluminate ############

  def midiIlluminate(self):
    self.enoMidiCtlr.simpleIlluminate(self.lightState)
    self.lightState += 1
    if self.lightState > 2: self.lightState = 0

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

      if control=="i9" and int(arg)==127: self.midiIlluminate(); return

      ctrlType = control[0]
      ctrlId   = int(control[1])
      ctrlVal  = int(arg)

      if ctrlType >= 'a' and ctrlType <= 'i' and ctrlVal == 127:
        row = ord(ctrlType) - ord('a')
        col = ctrlId - 1
        self.enoMidiCtlr.illumButton(row, col)
        print(row, col); return
 
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
