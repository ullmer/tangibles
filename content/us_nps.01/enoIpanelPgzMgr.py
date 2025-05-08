# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import traceback

import pgzero
print("pgzero version:",  pgzero.__version__)

#WIDTH, HEIGHT = 1700, 900
#WIDTH, HEIGHT = 1920, 1080
WIDTH, HEIGHT = 2100, 1150

from enoIpanelPgz     import *
from enoIpanelMidiMgr import *

def tup3(val): return (val, val, val) # convenience function for grayscale (three-element tuple)

############# enodia pygame zero interaction panel manager #############

class enoIpanelPgzMgr(enoIpanelMidiMgr): 
  matrixImgFn    = None
  matrixImgActor = None
  lastObservedPanelName = None
  
  #matrixCursorActive         = False
  matrixCursorActive          = True
  matrixCursorCurrentCoordIdx = (0, 0)          #tuple, initially 
  matrixCursorCurrentCoordPos = None
  matrixCursorDx,    matrixCursorDy     = (100, 100)
  matrixCursorWidth, matrixCursorHeight = (100, 100)
  matrixCursorXoff,  matrixCursorYoff   = (  0,   0)
  matrixCursorColor                     = tup3(200)
  matrixBrPos                           = (WIDTH, HEIGHT)

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    self.calcCursorCurrentCoordPos()

  ############# panel updated #############

  def calcCursorCurrentCoordPos(self):
    x0, y0 = self.matrixBrPos

    self.matrixCursorCurrentCoordPos = None

  ############# panel updated #############

  def panelUpdated(self): 
    cipan  = self.getCurrentInteractionPanel()
    currentName = cipan.getPanelName()

    if currentName == self.lastObservedPanelName: return False
    self.lastObservedPanelName = currentName
    return True

  ############# restage actors #############

  def restageActors(self): 
    cipan  = self.getCurrentInteractionPanel()
    imgFn  = cipan.getMatrixImageFn()

    cipan.screen       = screen #these two lines probably merit refactoring
    cipan.pgzIpanelMgr = self

    if self.matrixImgActor is None:
      self.matrixImgActor = Actor(imgFn, bottomright=self.matrixBrPos)
    else: 
      self.matrixImgActor.image   = imgFn
      self.matrixImgActor.opacity = 1. #remove transparency

  ############# drawMatrixCursor #############

  def drawMatrixCursor(self): 

    if self.matrixCursorActive is False: self.msg("drawMatrixCursor called, but flag disabled"); return

    mccci, mcccp = self.matrixCursorCurrentCoordIdx, self.matrixCursorCurrentCoordPos

    if mccci is None or mcccp is None:   self.msg("drawMatrixCusor: mccci or mcccp not initialized!"); return

    x, y = self.matrixCursorCurrentCoordPos
    cr   = Rect(x, y, self.matrixCursorWidth, self.matrixCursorHeight)
    draw.filled_rect(cr, self.matrixCursorColor)

    
  #matrixCursorColor                     = tup3(200)
  #matrixCursorCurrentCoordIdx = None #tuple, initially 
  #matrixCursorCurrentCoordPos = None
  #matrixCursorDx,    matrixCursorDy     = (100, 100)
  #matrixCursorWidth, matrixCursorHeight = (100, 100)
  #matrixCursorXoff,  matrixCursorYoff   = (  0,   0)

  ############# constructor #############

  #def __init__(self, **kwargs): 

  ############# midi cb #############

  def midiCB(self, control, arg): 
    super().midiCB(control, arg)

  ############# draw #############

  def draw(self): 
    if self.matrixImgActor is not None: self.matrixImgActor.draw()
    if self.matrixCursorActive:         self.drawMatrixCursor()

############# main #############

epim = enoIpanelPgzMgr()

print("=" * 70)

epi1 = enoIpanelPgz(tagFn = 'yaml/us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
epi2 = enoIpanelPgz(tagFn = 'yaml/cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

epim.registerIpanel(epi1, 0) #bootstrapping logic, to be reworked
epim.registerIpanel(epi2, 1)

def draw():   screen.clear(); epim.draw()
def update(): 
  epim.pollMidi()
  if epim.panelUpdated(): epim.restageActors() #probably to be renamed

### end ###
