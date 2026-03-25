# Enodia People and Themes: PyGame Zero mixin 
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-25

from enoPeopleThemes import *
import yaml

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

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.buildPeople()

  ############# build people #############

  def buildPeople(self):
    try:    
      abbrevs = self.getAbbrevs()
      for pa in abbrevs:
        fn = self.peoplePathPrefix + a
        a  = Actor(fn) 
        self.actors.append(a)
        
    except: self.err("buildPeople")

  ############# draw #############

  def draw(self):
    try:    for person in self.people: person.draw()
    except: self.err("draw")

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
