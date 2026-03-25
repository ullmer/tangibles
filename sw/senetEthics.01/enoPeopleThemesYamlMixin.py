# Enodia People and Themes: YAML mixin (largely populated by CoPilot)
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-25

from enoPeopleThemes import *

################### Enodia Person ###################

class EnoPersonYamlMixin:
#  name    = None # type: str | None 
#  abbrev  = None # type: str | None
#  era     = None # type: str | None
#  notes   = None # type: str | None
#  domains = None # type: list[str]  | None
#  themes  = None # type: list[str]  | None
#  colors  = None # type: ColorRings | None


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
