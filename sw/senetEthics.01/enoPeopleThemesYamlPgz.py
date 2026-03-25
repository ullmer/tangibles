# Enodia People & Themes, YAML+PGZ mixin-augmented class
# Brygg Ullmer (Clemson University) + CoPilot
# Begun 2026-03-25

from enoPeopleThemes          import *
from enoPeopleThemesYamlMixin import *
from enoPeopleThemesPgzMixin  import *

class EnoPersonYamlPgz(EnoPersonYamlMixin, EnoPersonPgzMixin, EnoPerson): pass
#  name    = None # type: str | None 
#  abbrev  = None # type: str | None
#  era     = None # type: str | None
#  notes   = None # type: str | None
#  domains = None # type: list[str]  | None
#  themes  = None # type: list[str]  | None
#  colors  = None # type: ColorRings | None
  
#  def draw(self):
#  def update(self):
#  def on_mouse_down(self, pos):    
#  def on_key_down(self, key, mod): 

################### Enodia Theme ###################

class EnoThemeYamlPgz( EnoThemeYamlMixin,  EnoThemePgzMixin,  EnoTheme):  pass

class EnoPeopleYamlPgz(EnoPeopleYamlMixin, EnoPeoplePgzMixin, EnoPeople): pass
class EnoThemesYamlPgz(EnoThemesYamlMixin, EnoThemesPgzMixin, EnoThemes): pass

### end ###
