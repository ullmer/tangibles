# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import traceback

import pgzero
print("pgzero version:",  pgzero.__version__)

WIDTH, HEIGHT = 1700, 900

from enoPgzIpanel     import *
from enoIpanelMidiMgr import *

############# enodia pygame zero interaction panel manager #############

class enoPgzIpanelMgr(enoIpanelMidiMgr): 
  matrixImgFn    = None
  matrixImgActor = None
  lastObservedPanelName = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

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
      self.matrixImgActor = Actor(imgFn)
    else: 
      self.matrixImgActor.image   = imgFn
      self.matrixImgActor.opacity = 1. #remove transparency

  ############# midi cb #############

  def midiCB(self, control, arg): 
    super().midiCB(control, arg)

  ############# draw #############

  def draw(self): 
    if self.matrixImgActor is not None: self.matrixImgActor.draw()

############# main #############

epim = enoPgzIpanelMgr()

print("=" * 70)

epi1 = enoPgzIpanel(tagFn = 'us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
epi2 = enoPgzIpanel(tagFn = 'cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

epim.registerIpanel(epi1, 0) #bootstrapping logic, to be reworked
epim.registerIpanel(epi2, 1)

def draw():   screen.clear(); epim.draw()
def update(): 
  epim.pollMidi()
  if epim.panelUpdated(): epim.restageActors() #probably to be renamed

### end ###
