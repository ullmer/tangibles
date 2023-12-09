# Enodia themes
# Brygg Ullmer, Clemson University
# Begun 2023-12-08

import yaml
from pygame import Rect
from pgzero.builtins import Actor, animate, keyboard
from enoActor import *

##################### enodia actor #####################

class enoThemePgz(enoActor):
  kwNum, pNum = None, None
  textKws     = None
  textPapers  = None

  txtOffset1 = (-50, -40)
  txtOffsetK = (-90,  18)
  txtOffsetP = (  0,  18)

  fontSizeKP = 32

  ############# constructor #############

  def __init__(self, imgFn, **kwargs): 

    self.__dict__.update(kwargs) 
    super(enoThemePgz, self).__init__(imgFn)

    self.textOffset = self.txtOffset1 #there is almost certainly a more elegant approach

  ############# pgzero draw #############

  def draw(self, screen):
    super(enoThemePgz, self).draw(screen) # call parent draw method

    x0, y0 = self.pos; dx, dy = self.actorDim; 

    if self.kwNum is not None: self.textKws    = str(self.kwNum)
    if self.pNum  is not None: self.textPapers = str(self.pNum)

    if self.textKws is not None: 
      tdx, tdy = self.txtOffsetK
      cx=x0+dx/2 + tdx; cy = y0+dy/2 + tdy

      screen.draw.text(self.textKws, centerx=cx, centery=cy, align="center",
                       fontsize=self.fontSizeKP, 
                       color=self.fgcolor, alpha=self.alpha)

    if self.textPapers is not None: 
      tdx, tdy = self.txtOffsetP
      cx=x0+dx/2 + tdx; cy = y0+dy/2 + tdy

      screen.draw.text(self.textPapers, centerx=cx, centery=cy, align="center",
                       fontsize=self.fontSizeKP, 
                       color=self.fgcolor, alpha=self.alpha)

############################################################### 
##################### enodia actor ensemble ###################
## plurality, but not of regular structure

class enoThemePgzEnsemble(enoActorEnsemble):
  themeList    = None
  themeObjDict = None
  objThemeDict = None
  objSelected  = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super(enoThemePgzEnsemble, self).__init__()
    self.themeList    = []
    self.themeObjDict = {}
    self.objThemeDict = {}

  ############# pgzero draw #############

  def saveState(self):
    for obj in self.themeList:
      name, pos = obj.text, obj.pos
      x, y      = pos
      print('%18s [%i,%i]' % (name+':', x,y))

  ############# pgzero draw #############

  def addTheme(self, themeName, kwNum, pNum, imgFn, **kwargs): 
    a = enoThemePgz(imgFn, pos=kwargs['pos'], kwNum=kwNum, pNum=pNum, text=themeName)

    self.themeList.append(a)
    self.themeObjDict[themeName] = a
    self.objThemeDict[a]         = themeName
    return a

  ############# pgzero draw #############

  def draw(self, screen): 
    for el in self.themeList: el.draw(screen)

  ######################### on_mouse_down #########################

  def on_mouse_down(self, pos):
    x,y=pos
    for el in self.themeList:
      if el.actor.collidepoint((x,y)): 
        name = self.objThemeDict[el]
        print("mouse selected:", name)
        self.objSelected = name

        if el.selectable: el.select()
        self.actorSelected = el

  ######################### on_mouse_move #########################

  def on_mouse_move(self, rel):
    if self.objSelected is not None:
      objName = self.objSelected 
      obj = self.themeObjDict[objName]
    
      x1, y1 = obj.pos
      dx, dy = rel
      x2, y2 = x1+dx,y1+dy
      obj.pos = (x2,y2)
      obj.actor.pos = obj.pos

  ######################### on_mouse_up #########################

  def on_mouse_up(self):
    if self.objSelected is not None: 
      obj = self.themeObjDict[self.objSelected]
      obj.deselect()
    self.objSelected = None

### end ###
