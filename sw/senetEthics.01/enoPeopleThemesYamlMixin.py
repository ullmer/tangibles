# Enodia People and Themes: YAML mixin (largely populated by CoPilot)
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-25

from enoPeopleThemes import *
import yaml

################### Enodia Person Yaml Mixin ###################

class EnoPersonYamlMixin:
#  name    = None # type: str | None 
#  abbrev  = None # type: str | None
#  era     = None # type: str | None
#  notes   = None # type: str | None
#  domains = None # type: list[str]  | None
#  themes  = None # type: list[str]  | None
#  colors  = None # type: ColorRings | None

  def load_from_yaml_dict(self, d: dict):
    self.name    = d.get("name")
    self.abbrev  = d.get("abbrev")
    self.era     = d.get("era")
    self.notes   = d.get("notes")
    self.domains = d.get("domains", [])
    self.themes  = d.get("themes", [])

    # RGB tuples
    if "colors" in d:
      self.colors = {
        k: tuple(v) for k, v in d["colors"].items()
      }

    return self

################### Enodia People Yaml Mixin ###################

class EnoPeopleYamlMixin:
 #people = None
  yamld  = None 

  def load_from_yaml(self, path: str):
    with open(path) as f: self.yamld = yaml.safe_load(f)

    for abbrev, entry in self.yamld["people"].items():
       p = EnoPersonYamlPgz().load_from_yaml_dict(entry)
       self.addPerson(p)

################### Enodia Theme ###################

class EnoTheme(EnoTok):
  name, color, themes = [None]*3

################### Enodia Themes ###################

class EnoThemes(AtaBase):
  themes = None

  def __init__(self):          self.themes = []

  def addTheme(self, theme): self.themes.append(person)

  def draw(self):
    for theme in self.themes: theme.draw()

### end ###
