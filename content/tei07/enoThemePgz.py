# Enodia themes
# Brygg Ullmer, Clemson University
# Begun 2023-12-08

import yaml, traceback
from pygame import Rect
from pgzero.builtins import Actor, animate, keyboard, keys
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
    #super(enoThemePgz, self).__init__(imgFn)
    super().__init__(imgFn)

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
  matrix       = None
  stateFn      = 'positions.yaml'

  shiftPressed = False
  shiftLPressed, shiftRPressed = False, False
  cursorRow, cursorCol         = 0, 0

  ex0, ey0     = 130, 75
  dx, dy       = 250, 102
  maxY         = 550
  animDuration = .5

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super(enoThemePgzEnsemble, self).__init__()
    self.themeList    = []
    self.themeObjDict = {}
    self.objThemeDict = {}

    self.matrix       = {} 
  
  ############# getMatrixContents #############

  def getMatrixContents(self, row, col):
    print("gmc", row, col)
    try:
      if self.matrix is None:         return None
      if row not in self.matrix:      return None
      if col not in self.matrix[row]: return None

      theme = self.matrix[row][col]
      obj   = self.themeObjDict[theme]
      return obj
    except:
      print("enoThemePgz getMatrixContents error", row, col); traceback.print_exc()
      return None

  ############# getMatrixContents #############

  def setMatrixContents(self, row, col, contents):
    print("smc", row, col)

    if self.matrix is None:         self.matrix = {}
    if row not in self.matrix:      self.matrix[row] = {}
    self.matrix[row][col] = contents
  
  ############# getCursorPos #############

  def getCursorPos(self):
    result = (self.cursorRow, self.cursorCol)
    return result

  ############# getCursorPos #############

  def getCursorObj(self):
    cursor = self.getMatrixContents(self.cursorRow, self.cursorCol)
    return cursor

  ############# selectCursor #############

  def selectCursor(self):
    try:
      cursor = self.getMatrixContents(self.cursorRow, self.cursorCol)
      if cursor is None: print("enoThemePgzEnsemble selectCursor: cursor empty for", self.cursorRow, self.cursorCol)
      else: cursor.select()
    except:
      print("enoThemePgz selectCursor error"); traceback.print_exc()

  ############# deselectCursor #############

  def deselectCursor(self):
    try:
      cursor = self.getMatrixContents(self.cursorRow, self.cursorCol)
      if cursor is None: print("enoThemePgzEnsemble deselectCursor: cursor empty for", self.cursorRow, self.cursorCol)
      else: cursor.deselect()
    except:
      print("enoThemePgz deselectCursor error"); traceback.print_exc()

  ############# moveCursor #############

  def moveCursor(self, dx, dy):
    y1, x1 = self.cursorRow, self.cursorCol
    x2, y2 = x1+dx, y1+dy
    self.deselectCursor()
    self.cursorRow, self.cursorCol = y2, x2
    self.selectCursor()

  ############# moveCursor #############

  def moveObject(self, dx, dy):
    cursorObj  = self.getCursorObj()
    cursorPos0 = self.getCursorPos()
    crow, ccol = cursorPos0
    scrPos0    = self.calcScreenPosition(crow,    ccol)
    scrPos1    = self.calcScreenPosition(crow+dy, ccol+dx)

    animate(cursorObj.actor, pos=scrPos1, tween='accel_decel', duration=self.animDuration)
    animate(cursorObj,       pos=scrPos1, tween='accel_decel', duration=self.animDuration)

    self.setMatrixContents(crow,    ccol,    None)

    self.cursorRow, self.cursorCol = crow + dy, ccol + dx

    cr2, cc2 = crow+dy, ccol+dx
    self.setMatrixContents(cr2, cc2, cursorObj)

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

  ############# calcScreenPosition #############

  def calcScreenPosition(self, row, col):
    x0, y0 = self.ex0,  self.ey0
    x1, y1 = x0+col*self.dx, y0+row*self.dy
    return (x1, y1)

  ############# loadEnoContent #############

  def loadEnoContent(self, ec, HEIGHT):
    c      = ec.tallyCountries()
    kwDict = ec.tallyKeywords()
    thPap  = ec.tallyThemes()

    x,  y    = self.ex0, self.ey0
    y0       = y
    row, col = 0, 0

    for theme in thPap:
      papers = thPap[theme]
      kcount = len(ec.themesKeywords[theme])
      pcount = len(papers)
      #print("%s: K%i P%i" % (theme, kcount, pcount))
      t = self.addTheme(theme, kcount, pcount, "tg01h2-theme", pos=(x,y))
      t.selImgFn = "tg01h2-theme-sel" #image backdrop when selected

      self.setMatrixContents(row, col, t)

      self.matrix[row][col] = theme

      y   += self.dy;   row += 1
      if y > self.maxY: row  = 0; y = y0; x += self.dx; col += 1

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
    if self.objSelected is not None: obj = self.themeObjDict[self.objSelected]
    self.mousePressed = False

  ######################### on_key_down #########################

  def on_key_down(self, key):
    #print("on_key_down", key)

    #if key == keys.SPACE:  print("space pressed")
    #if numTimesSpaceHit == 0:
    #      animate(a1, pos=(400, 500), tween='accel_decel', duration=.75)
    #else: animate(a2, pos=(500, 500), tween='accel_decel', duration=.75)

    if key == keys.LSHIFT: self.shiftLPressed = True
    if key == keys.RSHIFT: self.shiftRPressed = True

    if self.shiftLPressed or self.shiftRPressed: self.shiftPressed = True

    if not self.shiftPressed:
      if key == keys.RIGHT: self.moveCursor( 1, 0)
      if key == keys.LEFT:  self.moveCursor(-1, 0)
      if key == keys.UP:    self.moveCursor( 0,-1)
      if key == keys.DOWN:  self.moveCursor( 0, 1)
    else: #shift pressed
      if key == keys.RIGHT: self.moveObject( 1, 0)
      if key == keys.LEFT:  self.moveObject(-1, 0)
      if key == keys.UP:    self.moveObject( 0,-1)
      if key == keys.DOWN:  self.moveObject( 0, 1)

  ######################### on_key_down #########################

  def on_key_up(self, key):
    if key == keys.LSHIFT: self.shiftLPressed = False
    if key == keys.RSHIFT: self.shiftRPressed = False

    if not self.shiftLPressed and not self.shiftRPressed: self.shiftPressed = False

### end ###
