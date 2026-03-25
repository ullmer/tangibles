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

  def loadYamlDict(self, d: dict):
    try:
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
    except: self.err("load_from_yaml_dict")

################### Enodia People Yaml Mixin ###################

class EnoPeopleYamlMixin:
 #people = None
  yamld  = None 

  def loadYaml(self, yamlFn: str):
    try:
      yamlf = open(yamlFn, 'rt')
      self.yamld = yaml.safe_load(yamlf)
      yamlf.close()

      for abbrev, entry in self.yamld["people"].items():
        p = EnoPersonYamlPgz().loadYamlDict(entry)
        self.addPerson(p)
    except: self.err("loadYaml")

################### Enodia Theme ###################

class EnoThemeYamlMixin:

################### Enodia Themes ###################

class EnoThemesYamlMixin:
 #themes = None # type: list[EnoTheme]
  yamld = None

  def loadYaml(self, yamlFn: str):
    try:
      yamlf = open(yamlFn, 'rt')
      self.yamld = yaml.safe_load(yamlf)
      yamlf.close()

      for abbrev, entry in self.yamld["people"].items():
        p = EnoThemeYamlPgz().loadYamlDict(entry)
        self.addPerson(p)
    except: self.err("loadYaml")


### end ###
