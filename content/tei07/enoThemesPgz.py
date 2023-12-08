# Enodia themes
# Brygg Ullmer, Clemson University
# Begun 2023-12-08

import yaml
from pygame import Rect
from pgzero.builtins import Actor, animate, keyboard
from enoActor import *

##################### enodia actor #####################

class enoTheme(enoActor):
  pos        = (0,0)
  actorDim   = (100, 30)
  buttonRect = None
  textKws    = None
  textPapers = None

  txtOffset1 = (-60, -40)
  txtOffsetK = (-80,  10)
  txtOffsetP = ( 20,  10)

  fontSizeKP = 20

  ############# pgzero draw #############

  def draw(self, screen):
    super(enoTheme, self).draw(screen) # call parent draw method

    x0, y0 = self.pos; dx, dy = self.actorDim; 

    if self.textKws is not None: 
      tdx, tdy = self.txtOffsetK
      cx=x0+dx/2 + tdx; cy = y0+dy/2 + tdy

      screen.draw.text(self.textKws, centerx=cx, centery=cy, align="center",
                       fontsize=self.fontSizeKP, 
                       color=self.fgcolor, alpha=self.alpha)

    if self.textPapers is not None: 
      tdx, tdy = self.textPapers
      cx=x0+dx/2 + tdx; cy = y0+dy/2 + tdy

      screen.draw.text(self.textKws, centerx=cx, centery=cy, align="center",
                       fontsize=self.fontSizeKP, 
                       color=self.fgcolor, alpha=self.alpha)


############################################################### 
##################### enodia actor ensemble ###################
## plurality, but not of regular structure

class enoActorEnsemble:
  actorList     = None
  lastSelected  = None
  actorNameDict = None

  ############# constructor #############

  def __init__(self, **kwargs): 
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.actorList     = []
    self.actorNameDict = {}

  ############# pgzero draw #############

  def addActor(self, actorName, imgFn, **kwargs): 
    a = enoActor(imgFn, pos=kwargs['pos'])
    self.actorList.append(a)
    self.actorNameDict[actorName] = a
    return a

  ############# pgzero draw #############

  def draw(self, screen): 
    for actor in self.actorList: actor.draw(screen)

  ######################### on_mouse_down #########################

  def on_finger_down(self, finger_id, x, y):

    for actor in self.actorList:
      if actor.on_finger_down(finger_id, x, y):
        if self.lastSelected is not None: self.lastSelected.toggle()
        self.lastSelected = actor

### end ###
