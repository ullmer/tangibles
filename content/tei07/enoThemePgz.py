# Enodia themes
# Brygg Ullmer, Clemson University
# Begun 2023-12-08

import yaml, traceback
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
  stateFn      = 'positions.yaml'

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super(enoThemePgzEnsemble, self).__init__()
    self.themeList    = []
    self.themeObjDict = {}
    self.objThemeDict = {}

  ############# load state #############

  def loadState(self):
    f = open(self.stateFn, 'rt')
    y = yaml.safe_load(f)
    f.close()

    try:  
      for objName in y:
        try:  
          pos = y[objName]

          if objName in self.themeObjDict:
            obj = self.themeObjDict[objName]
            obj.pos = pos
            obj.actor.pos = obj.pos
        except:  print("enoThemePgzEnsemble loadState issue L1:"); traceback.print_exc()
    except:  print("enoThemePgzEnsemble loadState issue L2:"); traceback.print_exc()

  ############# save state #############

  def saveState(self):
    maxLen = 0
    for obj in self.themeList: 
      sl = len(obj.text)
      if sl>maxLen: maxLen=sl

    f = open(self.stateFn, 'wt')

    for obj in self.themeList:
      name, pos = obj.text, obj.pos
      x, y      = pos
      padlen    = maxLen-len(name)
      pad       = ' '*padlen
      f.write('%s:%s [%i,%i]\n' % (name, pad, x, y))

    f.close()

  ############# pgzero draw #############

  def addTheme(self, themeName, kwNum, pNum, imgFn, **kwargs): 
    a = enoThemePgz(imgFn, pos=kwargs['pos'], kwNum=kwNum, pNum=pNum, text=themeName)

    self.themeList.append(a)
    self.themeObjDict[themeName] = a
    self.objThemeDict[a]         = themeName
    return a

  ############# loadEnoContent #############

  def loadEnoContent(self, ec, HEIGHT, dx):
    c      = ec.tallyCountries()
    kwDict = ec.tallyKeywords()
    thPap  = ec.tallyThemes()

    x,  y  = 130, 75
    dy     = 100
    y0     = y

    for theme in thPap:
      papers = thPap[theme]
      kcount = len(ec.themesKeywords[theme])
      pcount = len(papers)
      #print("%s: K%i P%i" % (theme, kcount, pcount))
      t = self.addTheme(theme, kcount, pcount, "tg01h2-theme", pos=(x,y))
      t.selImgFn = "tg01h2-theme-sel" #image backdrop when selected
      y += dy
      if y > HEIGHT: y = y0; x += dx

  ############# pgzero draw #############

  def draw(self, screen): 
    for el in self.themeList: el.draw(screen)

  ######################### on_mouse_down #########################

  def on_mouse_down(self, pos):
    x,y=pos
    if self.objSelected is not None: 
      obj = self.themeObjDict[self.objSelected]
      obj.deselect()

    for el in self.themeList:
      if el.actor.collidepoint((x,y)): 
        name = self.objThemeDict[el]
        print("mouse selected:", name)
        self.objSelected = name

        if el.selectable: el.select()
        self.actorSelected = el
    self.mousePressed = True

  ######################### on_mouse_move #########################

  def on_mouse_move(self, rel):
    if self.objSelected is not None and self.mousePressed:
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
      #obj.deselect()
    #self.objSelected = None
    self.mousePressed = False

### end ###
