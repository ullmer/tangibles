# Enodia People & Themes, YAML+PGZ mixin-augmented class
# Brygg Ullmer (Clemson University) + CoPilot
# Begun 2026-03-25

from enoPeopleThemes          import *
from enoPeopleThemesMixinYaml import *
from enoPeopleThemesMixinPgz  import *

class EnoPersonYamlPgz(EnoPersonMixinYaml, EnoPersonMixinPgz, EnoPerson):  pass

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

################### Enodia Theme Yaml Pgz ###################

class EnoThemeYamlPgz( EnoThemeMixinYaml,  EnoThemeMixinPgz,  EnoTheme):  pass

############################################################# 
################### Enodia People Yaml Pgz ##################

class EnoPeopleYamlPgz(EnoPeopleMixinYaml, EnoPeopleMixinPgz, EnoPeople): 

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.personClass = EnoPersonYamlPgz

############################################################# 
################### Enodia Themes Yaml Pgz ##################

class EnoThemesYamlPgz(EnoThemesMixinYaml, EnoThemesMixinPgz, EnoThemes): 
  
  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.themeClass = EnoThemeYamlPgz

### end ###
