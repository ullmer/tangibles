#enoMidiController functionality toward poster interactivity
#Brygg Ullmer, Clemson University
#Begun 2024-03-17

import sys, os, traceback
from pygame import time
from enoMidiController import *
from functools   import partial

########################## poster midi controller ##########################

class posterMidiController:
  emc                 = None #enodia midi controller handle
  baseColorDict       = None
  highlightDict       = None

  dimensions          = [9, 9]
  highlightMultiplier = 6 

  ######################## constructor ######################## 

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.baseColorDict = {}; self.highlightDict = {}

    for i in range(self.dimensions[0]): 
      self.baseColorDict[i] = {} 
      self.highlightDict[i] = {} 
      for j in range(self.dimensions[1]): self.highlightDict[i][j] = False
      

    if self.emc is not None: #emc should be passed as an argument
      self.labelLaunchpad(self.emc)
      self.emc.registerExternalCB(self.buttonCB)

  ######################## set base color ######################## 

  def setBaseColor(self, x, y, r, g, b):
    try:
      self.baseColorDict[x][y]=[r,g,b]
    except:
      print("posterMidiController setBaseColor reports exception")
      traceback.print_exc()

  ######################## get base color ######################## 

  def getBaseColor(self, x, y):
    if self.baseColorDict == None:
      print("posterMidiController getBaseColor: baseColorDict is None!"); return None

    try:
      result = self.baseColorDict[x][y]
      return result
    except:
      return [0, 0, 0] #unlit if unassigned 
      #print("posterMidiController getBaseColor reports exception")
      #traceback.print_exc()

  ######################## highlight button ######################## 

  def highlightButton(self, x, y):
    col   = self.getBaseColor(x, y)
    hlcol = []
    for el in col: 
      v = el*self.highlightMultiplier
      if v > 63: v=63
      hlcol.append(v)

    r,g,b = hlcol
    self.emc.setLaunchpadXYColor(x,y,r,g,b)

  ######################## highlight button ######################## 

  def normalLightButton(self, x, y):
    r,g,b = self.getBaseColor(x, y)
    self.emc.setLaunchpadXYColor(x,y,r,g,b)

  ######################## button callback ######################## 

  def buttonCB(self, emc, control, arg):
    x, y    = emc.addr2coord(control)

    #r, g, b = [63, 63, 63]
    #emc.setLaunchpadXYColor(x, y, r, g, b)

    isButtonHighlighted = self.highlightDict[x,y]
    if isButtonHighlighted: 
      self.highlightDict[x,y] = False
      self.normalLightButton(x,y)
    else:
      self.highlightDict[x,y] = True
      self.highlightButton(x,y)

  ######################## labelLaunchpad ######################## 
  
  def labelLaunchpad(self, emc):
  
    for i in range(4): self.setBaseColor(i, 0, 13, 13, 13)
  
    for j in range(4):
      for i in [0, 4]: self.setBaseColor(i, j+1, 8,   8, 8)
      for i in [1, 5]: self.setBaseColor(i, j+1, 0,   8, 2)
      for i in [2, 6]: self.setBaseColor(i, j+1, 10, 10, 0)
      for i in [3, 7]: self.setBaseColor(i, j+1, 15,  5, 0)
    self.setBaseColor(0, 5, 8, 8, 8)
    self.setBaseColor(1, 5, 0, 8, 2)
  
    for i in [2, 7]: self.setBaseColor(i, 5, 4, 4, 4)
    self.setBaseColor(3, 5,  0, 12,  0) #na
    self.setBaseColor(4, 5,  0,  0, 12) #eu
    self.setBaseColor(5, 5, 14,  0,  0) #as
    self.setBaseColor(6, 5, 14, 14,  0) #me
  
    for j in range(3):
      for i in [0, 2, 4, 6]: self.setBaseColor(i, j+6, 0, 0, 8)
      for i in [1, 3, 5, 7]: self.setBaseColor(i, j+6, 8, 8, 8)

    for i in range(self.dimensions[0]): 
      for j in range(self.dimensions[1]): 
        r,g,b = self.getBaseColor(i, j)
        self.emc.setLaunchpadXYColor(i,j,r,g,b)
  
#### main ####
  
emc = enoMidiController('nov_launchpad_x')
#emc = enoMidiController('nov_launchpad_mk2')
emc.clearLights()

pmc = posterMidiController(emc=emc)

while True:
  emc.pollMidi()
  time.wait(100)

### end ###
