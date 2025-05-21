# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

from enoIpanelPgzMgr import *

WIDTH, HEIGHT = 2100, 1150

############# main #############

epim = enoIpanelPgzMgr()

print("=" * 70)

epi1 = enoIpanelPgz(tagFn = 'yaml/us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
epi2 = enoIpanelPgz(tagFn = 'yaml/cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

epim.registerIpanel(epi1, 0) #bootstrapping logic, to be reworked
epim.registerIpanel(epi2, 1)
  
def draw():   
  screen.clear(); 
  epim.draw(screen)

def update(): 
  epim.pollMidi()
  if epim.panelUpdated(): epim.restageActors(screen) #probably to be renamed

### end ###
