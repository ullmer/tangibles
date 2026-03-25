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

class EnoPeopleYamlMixin:
  def draw(self): pass

################### Enodia Theme ###################

class EnoThemeYamlMixin:
  def draw(self): pass

################### Enodia Themes ###################

class EnoThemesPgzMixin:
  def draw(self):
    for theme in self.themes: theme.draw()

### end ###
