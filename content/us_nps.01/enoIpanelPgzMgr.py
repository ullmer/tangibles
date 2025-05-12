# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import traceback
import pgzero
print("pgzero version:",  pgzero.__version__)

#WIDTH, HEIGHT = 1700, 900
#WIDTH, HEIGHT = 1920, 1080
WIDTH, HEIGHT = 2100, 1150

from pgzero.builtins import Actor, animate, keyboard

from enoIpanelPgz     import *
from enoIpanelMidiMgr import *
from enoActorScaled   import *

def tup3(val): return (val, val, val) # convenience function for grayscale (three-element tuple)

############# enodia pygame zero interaction panel manager #############

class enoIpanelPgzMgr(enoIpanelMidiMgr): 
  matrixImgFn         = None
  matrixImgActor      = None
  matrixImgActorScale = 1.
  lastObservedPanelName = None
  
  #matrixCursorActive         = False
  matrixCursorActive          = True
  matrixCursorCurrentCoordIdx = (0, 0)          #tuple, initially 
  matrixCursorCurrentCoordPos = None
  matrixCursorDx,    matrixCursorDy     = (253, 142)
  matrixCursorWidth, matrixCursorHeight = (253, 142)
  matrixCursorXoff,  matrixCursorYoff   = (  0,   0)
  matrixCursorColor                     = tup3(200)
  matrixBrPos                           = (WIDTH, HEIGHT)

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelPgzMgr error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelPgzMgr msg: "   + str(msgStr))

  ############# panel updated #############

  def calcCursorCurrentCoordPos(self):
    try:
      x0, y0 = self.matrixBrPos
      i,  j  = self.getCurrentCoord()

      self.matrixCursorCurrentCoordPos = None
      ipan = self.getCurrentInteractionPanel()
      w, h = ipan.getDim()

      dx = (w - i) * self.matrixCursorDx + self.matrixCursorXoff
      dy = (h - j) * self.matrixCursorDy + self.matrixCursorYoff

      #print("ccccp:", dx, dy)
      x1, y1 = x0-dx, y0-dy
      result = (x1, y1)
      #self.matrixCursorCurrentCoordPos = result
      return result

    except: self.err("calcCursorCurrentCoordPos")
  
  #matrixCursorColor                     = tup3(150)
  #matrixCursorCurrentCoordIdx = None #tuple, initially 
  #matrixCursorCurrentCoordPos = None
  #matrixCursorDx,    matrixCursorDy     = (100, 100)
  #matrixCursorWidth, matrixCursorHeight = (100, 100)
  #matrixCursorXoff,  matrixCursorYoff   = (  0,   0)

  ############# panel updated #############

  def panelUpdated(self): 
    try:
      cipan  = self.getCurrentInteractionPanel()
      currentName = cipan.getPanelName()

      if currentName == self.lastObservedPanelName: return False
      self.lastObservedPanelName = currentName
      return True
    except: self.err("panelUpdated")

  ############# restage actors #############

  def restageActors(self): 
    cp = self.calcCursorCurrentCoordPos()
    if cp != self.getCurrentCoord():
      #animate

      self.setCurrentCoord(cp)

    cipan  = self.getCurrentInteractionPanel()
    imgFn  = cipan.getMatrixImageFn()

    cipan.screen       = screen #these two lines probably merit refactoring
    cipan.pgzIpanelMgr = self

    if self.matrixImgActor is None:
      self.matrixImgActor = enoActorScaled(imgFn, bottomright=self.matrixBrPos, scale=1.)
    else: 
      self.matrixImgActor.image   = imgFn
      self.matrixImgActor.opacity = 1. #remove transparency

  ############# drawMatrixCursor #############

  def drawMatrixCursor(self, screen): 

    if self.matrixCursorActive is False: 
      self.msg("drawMatrixCursor called, but flag disabled"); return

    try:
      x, y = self.calcCursorCurrentCoordPos()
      cr   = Rect((x, y), (self.matrixCursorWidth, self.matrixCursorHeight))
      #if self.verbose: #print("DMC: ", x, y, self.matrixCursorWidth, \
      #   self.matrixCursorHeight, self.matrixCursorColor)
      screen.draw.filled_rect(cr, self.matrixCursorColor)

    except: self.err("drawMatrixCursor")
    
  ############# constructor #############
  #def __init__(self, **kwargs): 

  ############# midi cb #############

  def midiCB(self, control, arg): 
    super().midiCB(control, arg)

  ############# change matrix scale #############

  def changeMatrixScale(self, scale): 
    if self.matrixImgActor is None: 
      self.msg("changeMatrixScale called, but matrix actor not initiated"); return None

    self.matrixImgActorScale  = scale
    self.matrixImgActor.scale = scale

  ############# draw #############

  def draw(self, screen): 
    if self.matrixCursorActive:         self.drawMatrixCursor(screen)
    if self.matrixImgActor is not None: self.matrixImgActor.draw()

############# main #############

epim = enoIpanelPgzMgr()

print("=" * 70)

epi1 = enoIpanelPgz(tagFn = 'yaml/us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
epi2 = enoIpanelPgz(tagFn = 'yaml/cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

epim.registerIpanel(epi1, 0) #bootstrapping logic, to be reworked
epim.registerIpanel(epi2, 1)
  
def draw():   
  epim.changeMatrixScale(.5)
  screen.clear(); epim.draw(screen)

def update(): 
  epim.pollMidi()
  if epim.panelUpdated(): epim.restageActors() #probably to be renamed

### end ###
