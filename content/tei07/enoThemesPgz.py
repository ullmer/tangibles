# Enodia themes
# Brygg Ullmer, Clemson University
# Begun 2023-12-08

import yaml
from pygame import Rect
from pgzero.builtins import Actor, animate, keyboard
from enoActor import *

##################### enodia actor #####################

class enoThemePgz(enoActor):
  pos        = (0,0)
  actorDim   = (100, 30)
  buttonRect = None
  textKws    = None
  textPapers = None

  txtOffset1 = (-60, -40)
  txtOffsetK = (-80,  10)
  txtOffsetP = ( 20,  10)

  fontSizeKP = 20

  ############# constructor #############

  def __init__(self, imgFn, **kwargs): 

    self.__dict__.update(kwargs) 
    super(enoThemePgz, self).__init__(imgFn, kwargs)

    self.primaryTextOffset = self.txtOffset1 #there is almost certainly a more elegant approach

  ############# pgzero draw #############

  def draw(self, screen):
    super(enoThemePgz, self).draw(screen) # call parent draw method

    x0, y0 = self.pos; dx, dy = self.actorDim; 

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
  themeList     = None
  lastSelected  = None
  themeNameDict = None

  ############# pgzero draw #############

  def addTheme(self, themeName, imgFn, **kwargs): 
    a = enoThemePgz(imgFn, pos=kwargs['pos'])
    self.themeList.append(a)
    self.themeNameDict[themeName] = a
    return a

### end ###
