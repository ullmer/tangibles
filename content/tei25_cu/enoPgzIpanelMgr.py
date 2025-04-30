# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import traceback

WIDTH, HEIGHT = 1500, 800

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
    if self.matrixImgActor is None:
      self.matrixImgActor = Actor(imgFn)
    else: 
      self.matrixImgActor.image = imgFn

  ############# draw #############

  def draw(self): 
    if self.matrixImgActor is not None: self.matrixImgActor.draw()

############# main #############

epim = enoPgzIpanelMgr()

print("=" * 70)

eim1 = enoIpanelMidi(tagFn = 'us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
eim2 = enoIpanelMidi(tagFn = 'cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

epim.registerIpanel(eim1, 0) #bootstrapping logic, to be reworked
epim.registerIpanel(eim2, 1)

def draw():   epim.draw()
def update(): 
  epim.pollMidi()
  if epim.panelUpdated(): epim.restageActors() #probably to be renamed

### end ###
