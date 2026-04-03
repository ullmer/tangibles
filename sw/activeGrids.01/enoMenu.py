# Enodia menu-like elements -- sometimes backed by Pygame Zero, 
#  sometimes by physical buttons, sometimes by other variants.
# First approximation, albeit too specific to Pygame Zero
# Brygg Ullmer, Clemson University
# Begun 2024-08-11

import yaml
import os
import traceback

from   enoButton      import *
from   enoButtonArray import *

##################### enodia menu #####################

class enoMenu:
  basePos    = (50,50)

  animTargetsSet  = False #animation target positions set
  requestAnim     = None  #request child elements to start at ~home position, rather than to immediately deploy to place
  motionAnimTween = 'accel_decel'
  animDuration    = .5

  buttonDim  = (100, 100)
  #bgcolor1   = (0, 0, 130)
  #bgcolor2   = (50, 50, 250)
  bgcolor1   = (20, 20, 20)
  bgcolor2   = (100, 100, 100)
  fgcolor    = "#bbbbbb"

  alpha      = .8
  fontSize   = 36
  angle      = 0
  dx, dy     = 0, 105
  buttonsActive = True

  yamlFn     = None
  yamlD      = None
  yamlMenuD  = None

  drawText   = False
  drawImg    = False
  drawAdapt  = True   # if True, will render text and/or image only when specified

  whichMenuName = "homeMenu"

  autoBuildMenu = True
  verbose       = False

  enoButtonArr  = None

  ############# constructor #############

  def __init__(self, whichMenuName=None, **kwargs): 

    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not

    if whichMenuName is not None: self.whichMenuName = whichMenuName
    self.loadYaml()

    if self.autoBuildMenu: self.buildMenu()

  ############# error message #############

  def err(self, msg): print("enoMenu error:" + msg)
  def msg(self, msg): print("enoMenu msg:  " + msg)

  ############# load yaml #############

  def loadYaml(self):
    if self.yamlFn is None:                  err("loadYaml: yaml filename undefined"); return
    if os.path.exists(self.yamlFn) == False: err("loadYaml: yaml file not found:" + self.yamlFn); return

    f = open(self.yamlFn, 'rt')
    self.yamlD = yaml.safe_load(f)
    f.close()

    if 'animist' not in self.yamlD:  err("loadYaml: animist not found in yaml" + self.yamlFn); return

    ad = self.yamlD['animist']

    if self.whichMenuName not in ad: err("loadYaml: %s menu not found in yaml %s" % (self.whichMenuName, self.yamlFn)); return

    self.yamlMenuD = ad[self.whichMenuName]

  ############# build menu #############

  def buildMenu(self):
    if self.yamlMenuD is None: err("buildMenu: yaml menu datastructure not found"); return

    textHandles = []; imageFns = []

    for menuEntry in self.yamlMenuD:
      try:    name = menuEntry['name']; imageFn = menuEntry['imageFn']
      except: err("buildMenu: menuEntry parsing issue"); traceback.print_exc(); return
      textHandles.append(name); imageFns.append(imageFn)

    self.msg("buildMenu: %s || %s" % (str(textHandles), str(imageFns)))

    self.enoButtonArr = enoButtonArray(textHandles,  imageFns = imageFns, buttonDim = self.buttonDim,
                          dx = self.dx, dy = self.dy, basePos = self.basePos, 
                          drawText = self.drawText,  drawImg = self.drawImg, drawAdapt = self.drawAdapt,
                          bgcolor1 = self.bgcolor1, bgcolor2 = self.bgcolor2,  fgcolor = self.fgcolor, 
                          alpha    = self.alpha,    fontSize = self.fontSize,    angle = self.angle,
                          requestAnim  = self.requestAnim, motionAnimTween = self.motionAnimTween,
                          animDuration = self.animDuration);

    self.enoButtonArr.addCallback(self.buttonCb)

  ############# expand/contract #############

  def expandContract(self): 
    if self.enoButtonArr is None: self.err("expandContract called, but enoButtonArr not populated.  ignoring"); return
    self.enoButtonArr.expandContract()

  ############# button callback #############

  def buttonCb(self, whichButtonPressed):
    self.msg("buttonCB:" + whichButtonPressed)

  ############# animate to target #############

  def animateToTarget(self): 
    if self.animTargetsSet == False:  self.err("animateToTarget: targets not set!"); return
    if self.enoButtonArr is None: self.err("animateToTarget: enoButtonArray is empty!"); return

    self.activeAnim = self.enoButtonArr.animateToTargets()

  ############# draw #############

  def draw(self,          screen): self.enoButtonArr.draw(screen)

  def on_mouse_down(self, pos):    
    if self.buttonsActive: self.enoButtonArr.on_mouse_down(pos)

### end ###
