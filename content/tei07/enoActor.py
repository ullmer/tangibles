# Enodia Button-like elements -- sometimes backed by Pygame Zero, 
#  sometimes by physical buttons, sometimes by other variants.
# Brygg Ullmer, Clemson University
# Begun 2022-02-22

# https://pygame-zero.readthedocs.io/en/stable/ptext.html
# https://pythonprogramming.altervista.org/pygame-4-fonts/

import yaml
from pygame import Rect
from pgzero.builtins import Actor, animate, keyboard
#https://stackoverflow.com/questions/55438239/name-actor-is-not-defined

##################### enodia actor #####################

class enoActor:
  pos         = (0,0)
  actorDim    = (100, 30)
  drawRect    = False
  buttonRect  = None
  text        = None
  textOffset  = (0, 0)

  bgcolor1   = (0, 0, 130)
  bgcolor2   = (50, 50, 250)
  #fgcolor    = "#bbbbbb"
  fgcolor    = "#eeeeee"

  alpha      = .8
  fontSize   = 36
  imgFn      = None
  actor      = None # for image/sprite
  abbrev     = None # name/identity/handle

  toggleMode  = True
  toggleState = False
  verbose     = False

  ############# constructor #############

  def __init__(self, imgFn, **kwargs): 

    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.actor     = Actor(imgFn)
    self.actor.pos = self.pos

  ############# pgzero draw #############

  def getAbbrev(self):
    return self.abbrev

  ############# pgzero draw #############

  def draw(self, screen):
    self.actor.draw()

    if self.drawRect: screen.draw.filled_rect(self.buttonRect, bgcolor)

    if self.text is not None: 
      tdx, tdy = self.textOffset

      x0, y0 = self.pos; dx, dy = self.actorDim; 
      cx=x0+dx/2 + tdx; cy = y0+dy/2 + tdy

      screen.draw.text(self.text, centerx=cx, centery=cy, align="center",
                       fontsize=self.fontSize, 
                       color=self.fgcolor, alpha=self.alpha)

    return 

    #if self.toggleMode and self.toggleState: bgcolor = self.bgcolor2
    #else:                                    bgcolor = self.bgcolor1

  ############# nudge #############

  def nudgeY(self, dy): 
    bpx, bpy = self.pos
    self.pos = (bpx, bpy+dy)
    self.buttonRect = Rect(self.pos, self.actorDim)

  def nudgeXY(self, dx, dy): 
    bpx, bpy = self.pos
    self.pos = (bpx+dx, bpy+dy)
    self.buttonRect = Rect(self.pos, self.actorDim)

  ######################### on_mouse_down #########################

  def toggle(self):
    if self.toggleState: self.toggleState = False
    else:                self.toggleState = True

  ######################### on_mouse_down #########################

  def on_finger_down(self, finger_id, x, y):
    if self.verbose: print("ofd:", x, y)
    if self.actor.collidepoint((x,y)): 
      if self.abbrev is not None: print(self.abbrev, "pressed1")
      else:                       print(self.actorTextPrimary, "pressed2")
      self.toggle()
      return True

    return False

############################################################### 
##################### enodia actor array #####################
## fixed, regular grid

class enoActorArray:
  pos    = (0,0) #30, 327
  actorDim  = (100, 30)
  #dx, dy     = 190, 0
  dx, dy     = 55, 0

  textArray    = None
  actorArray   = None
  lastSelected = None

  yamlFn, yamlF, yamlD = [None] * 3

  ############# constructor #############

  def __init__(self, yamlFn, **kwargs): 
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.actorArray = []
    self.parseYaml(yamlFn)

    idx = 0

    bpx, bpy = self.pos

    if self.textArray is None: return

    for text in self.textArray:
      but = enoActor(text, pos = (bpx+idx*self.dx, bpy+idx*self.dy),
                      actorDim = self.actorDim)
      self.actorArray.append(but); idx += 1

  ############# yaml warning #############

  def yamlWarn(self, message): 
    print("enoActor parseYaml warning: ", message)

  ############# parse yaml #############

  def parseYaml(self, yamlFn): 

    self.yamlFn = yamlFn
    self.yamlF  = open(yamlFn, 'r+t')
    yd = self.yamlD  = yaml.safe_load(self.yamlF)

    if 'panel' not in yd: self.yamlWarn("panel not present"); return
    ydp = yd['panel']

    if 'buttons' not in ydp: self.yamlWarn("panel:buttons not present"); return
    ydpb = ydp['buttons']

    self.yamlWarn(str(ydpb))

  ############# pgzero draw #############

  def draw(self, screen): 
    for actor in self.actorArray: actor.draw(screen)

  ######################### on_mouse_down #########################

  def on_mouse_down(self, pos):
    for actor in self.actorArray:
      if actor.on_mouse_down(pos):
        if self.lastSelected is not None: self.lastSelected.toggle()
        self.lastSelected = actor

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

    if 'drawRect'    in kwargs: a.drawRect   = kwargs['drawRect']
    if 'text'        in kwargs: a.text       = kwargs['text']
    if 'textOffset'  in kwargs: a.textOffset = kwargs['textOffset']

    self.actorList.append(a)
    self.actorNameDict[actorName] = a
    return a

  ############# pgzero draw #############

  def draw(self, screen): 
    for actor in self.actorList: actor.draw(screen)

  ######################### on_mouse_down #########################

  #def on_mouse_down(self, x, y):
  #  for actor in 

  ######################### on_mouse_down #########################

  def on_finger_down(self, finger_id, x, y):

    for actor in self.actorList:
      if actor.on_finger_down(finger_id, x, y):
        if self.lastSelected is not None: self.lastSelected.toggle()
        self.lastSelected = actor

### end ###
