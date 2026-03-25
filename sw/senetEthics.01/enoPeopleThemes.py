# Broad contours of "key objects of interest" toward
#  Computing, Ethics, and Global Society example
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-24

from ataBase  import *
from enoActor import *
from typing import TypedDict

################### Enodia Token ###################

class EnoTok(EnoActor):
#  def draw(self):   
#  def update(self): 
#  def on_mouse_down(self, pos):    
#  def on_key_down(self, key, mod): 

################### Color support classes for EnoPerson, EnoTheme ###################

RGB = tuple[int, int, int]

class ColorRings(TypedDict):
  outer:  RGB
  middle: RGB
  inner:  RGB

################### Enodia Person ###################

class EnoPerson(EnoTok):
  name    = None # type: str | None 
  abbrev  = None # type: str | None
  era     = None # type: str | None
  notes   = None # type: str | None
  domains = None # type: list[str]  | None
  themes  = None # type: list[str]  | None
  colors  = None # type: ColorRings | None

  personClass = None # toward mixin integration

################### Enodia Theme ###################

class EnoTheme(EnoTok):
  name    = None # type: str | None 
  colors  = None # type: ColorRings | None
  themes  = None # type: list[str]  | None

  themeClass = None # toward mixin integration

################### Enodia People ###################

class EnoPeople(AtaBase):
  people = None # type: list[EnoPerson]

  def __init__(self):          self.people = []

  def addPerson(self, person): 
    try:    self.people.append(person)
    except: self.err("addPerson")

################### Enodia Themes ###################

class EnoThemes(AtaBase):
  themes = None # type: list[EnoTheme]

  def __init__(self):          self.themes = []

  def addTheme(self, theme): 
    try:    self.themes.append(theme)
    except: self.err("addTheme")

### end ###
