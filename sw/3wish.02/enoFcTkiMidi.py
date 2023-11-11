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

  useTki  = True 
  useMidi = True

  tkiActive      = None
  midiActive     = None

  functoolsWorking = None  #Many (etc.) FreeCAD users may not have all 
  tkiWorking       = None  # relevant Python packages or (for MIDI)
  pilWorking       = None  # devices installed.  This shouldn't cause
  midiWorking      = None  # things to break

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.useTki:  self.activateTki();  self.buildTki()
    if self.useMidi: self.activateMidi(); self.buildMidi()

  ############# activate Tkinter #############

  def activateTki(self):
    try:    
      from tkinter   import *
      self.tkiWorking = True #let's initially assume that successful import 
                             #indicates "working." Later with embedded devices
			     #in particular, this may wish to become more nuanced.
    except: 
      self.tkiWorking = False
      self.reportError('activateTki', 'tkinter import unsuccessful.')

    try: 
      from functools import partial
      self.functoolsWorking = True
    else: 
      self.functoolsWorking = False
      self.reportError('activateTki', 'functools import (for callback "partials") unsuccessful.')

    #import PIL.Image, PIL.ImageTk #image manipulation package


  ############# activate Midi #############

view, doc, sg, root = genViewDocSgRoot()


### end ###
