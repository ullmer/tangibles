# Interaction panel MIDI manager
# Brygg Ullmer, Clemson University
# Begun 2025-04-28

import sys, os, yaml, traceback

############# enodia interaction panel manager #############

class enoIpanelMgr:

  verbose = False
  #verbose = True

  sidebar_bottom = 1
  sidebar_right  = 2
  sidebarButtonCurrentlyActive = None

  currentCoord = (0, 0)

  ipanelSidebarDict = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ############# error, msg #############

  def err(self, msgStr): print("enoIpanelMgr error: " + str(msgStr)); traceback.print_exc(); 
  def msg(self, msgStr): print("enoIpanelMgr msg: "   + str(msgStr))

  ############# set, get current coord #############

  def setCurrentCoord(self, newCoord): self.currentCoord = newCoord
  def getCurrentCoord(self):    return self.currentCoord 

  ############# register interaction panel #############

  def registerIpanel(self, ipanelHandle, whichSidebarButton):
    if self.ipanelSidebarDict is None:
      self.ipanelSidebarDict = {}

    self.ipanelSidebarDict[whichSidebarButton] = ipanelHandle
  
  ############# get registered interaction panel #############

  def getRegisteredIpanel(self, whichSidebarButton):
    if self.ipanelSidebarDict is None:                   return None
    if whichSidebarButton not in self.ipanelSidebarDict: return None
    result = self.ipanelSidebarDict[whichSidebarButton]
    return result

  ############# get current interaction panel #############
 
  def getCurrentInteractionPanel(self):
    try:
      whichSidebarButton = self.sidebarButtonCurrentlyActive 
      cipan              = self.getRegisteredIpanel(whichSidebarButton)
      return cipan
    except: self.err("getCurrentInteractionPanel")

  ############# is sidebar button #############

  def isSidebarButton(self, whichButton): 
    try:
      if len(whichButton) != 2: return False
      w0, w1 = whichButton
      if w1 == '9' and 'a' <= w0 <= 'h': return True
      return False
    except: self.err("isSidebarButton " + str(whichButton))

  def isMatrixButton(self, whichButton): 
    try:
      if len(whichButton) != 2: return False
      w0, w1 = whichButton
      if '0' <= w1 < '9' and 'a' <= w0 <= 'h': return True
      return False
    except: self.err("isSidebarButton " + str(whichButton))

  def getSidebarButtonVal(self, whichButton): 
    try:
      if len(whichButton) != 2: return None
      result = ord(whichButton[0]) - ord('a')
      return result
    except: self.err("getSidebarButtonVal" + str(whichButton))

############# main #############

if __name__ == "__main__":
  print("=" * 70)
  eim1 = enoIpanel(tagFn = 'us-bea.yaml',     casePaired=True,  autolaunchMidi=False)
  eim2 = enoIpanel(tagFn = 'cspan-tags.yaml', casePaired=False, autolaunchMidi=False)

  eimm = enoIpanelMgr()
  eimm.registerIpanel(eim1, 0) #bootstrapping logic, to be reworked
  eimm.registerIpanel(eim2, 1)

### end ###
