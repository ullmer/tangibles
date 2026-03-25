# Broad contours of "key objects of interest" toward
#  Computing, Ethics, and Global Society example
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-24

from ataBase  import *
from enoActor import *

################### Enodia Token ###################

class EnoTok(EnoActor):
  def draw():   pass
  def update(): pass

  #def on_mouse_down(pos):    pass
  #def on_key_down(key, mod): pass

################### Enodia Person ###################

class EnoPerson(EnoTok):
  name    = None # type: str | None 
  abbrev  = None # type: str | None
  era     = None # type: str | None
  notes   = None # type: str | None
  domains = None # type: list[str] | None
  themes  = None # type: list[str] | None
  colors  = None # type: dict[str, list[int]] | None

################### Enodia Theme ###################

class EnoTheme(EnoTok):
  name, color, themes = [None]*3

################### Enodia People ###################

class EnoPeople(AtaBase):
  people = None

  def __init__(self):          self.people = []

  def addPerson(self, person): self.people.append(person)

  def draw(self):
    for person in self.people: person.draw()

################### Enodia Themes ###################

class EnoThemes(AtaBase):
  themes = None

  def __init__(self):          self.themes = []

  def addTheme(self, theme): self.themes.append(person)

  def draw(self):
    for theme in self.themes: theme.draw()

### end ###
