# Enodia People & Themes, YAML+PGZ mixin-augmented class
# Brygg Ullmer (Clemson University) + CoPilot
# Begun 2026-03-25

from enoPeopleThemes          import *
from enoPeopleThemesYamlMixin import *
from enoPeopleThemesPgzMixin  import *

class EnoPersonYamlPgz(EnoPersonYamlMixin, EnoPersonPgzMixin, EnoPerson): pass
class EnoThemeYamlPgz( EnoThemeYamlMixin,  EnoThemePgzMixin,  EnoTheme):  pass

class EnoPeopleYamlPgz(EnoPeopleYamlMixin, EnoPeoplePgzMixin, EnoPeople): pass
class EnoThemesYamlPgz(EnoThemesYamlMixin, EnoThemesPgzMixin, EnoThemes): pass

### end ###
