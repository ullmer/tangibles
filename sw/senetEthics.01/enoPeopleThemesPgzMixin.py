# Enodia People and Themes: PyGame Zero mixin 
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-25

from pgzero.builtins import Actor, animate, keyboard, keys
import yaml

from enoPeopleThemes import *

################### Enodia Person Pgz Mixin ###################

class EnoPersonPgzMixin:
# name    = None # type: str | None 
# abbrev  = None # type: str | None
# era     = None # type: str | None
# notes   = None # type: str | None
# domains = None # type: list[str]  | None
# themes  = None # type: list[str]  | None
# colors  = None # type: ColorRings | None

  def draw(self): pass

################### Enodia People Yaml Mixin ###################

class EnoPeoplePgzMixin:
# people = None # type: list[EnoPerson]
  actors = None # type: list[Actor]
  peoplePathPrefix = "people/"
  basePos = (300, 500)
  dx = 100
  selectedActor = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.buildActors()

  ############# build people #############

  def buildActors(self):
    try:    
      self.actors = []
      x, y = self.basePos
      abbrevs = self.getAbbrevs()

      for pa in abbrevs:
        fn = self.peoplePathPrefix + a
        a  = Actor(fn) 
        self.actors.append(a)
        a.pos = (x, y); x += self.dx 
        
    except: self.err("buildActors")

  ############# draw #############

  def draw(self):
    try:    for a in self.actors: a.draw()
    except: self.err("draw")

  ############# on_mouse_down #############

  def on_mouse_down(self, pos): 
    try:    
      for a in self.actors:
        if a.collidepoint(pos): 
          self.selectedActor = a
    except: self.err("on_mouse_down")

  ############# on_mouse_down #############

  def on_mouse_up(self): 
    try:    
      animate(self.selectedActor, pos=(100,100), tween='accel_decel')
      self.selectedActor = None
    except: self.err("on_mouse_up")

  ############# on_mouse_move #############

  def on_mouse_move(self, rel):
    try:    
      if self.selectedActor is not None: 
        dx, dy = rel
        x,  y  = self.selectedActor.pos
        x += dx; y += dy
        self.selectedActor.pos = (x,y)
    except: self.err("on_mouse_up")

####################################################
################### Enodia Theme ###################

class EnoThemePgzMixin:
  def draw(self): pass

################### Enodia Themes ###################

class EnoThemesPgzMixin:
# themes = None # type: list[EnoTheme]

  def draw(self):
    try:    for theme in self.themes: theme.draw()
    except: self.err("draw")

### end ###

