# Enodia People and Themes: YAML mixin (largely populated by CoPilot)
# Brygg Ullmer, Clemson University
# Begun 2026-03-25

import yaml
from typing          import Optional

from enoPeopleThemes import *
from enoOSsupport    import *

################### Enodia Person Yaml Mixin ###################

class EnoPersonMixinYaml:
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
    except: self.err("loadYamlDict")

################### Enodia People Yaml Mixin ###################

class EnoPeopleMixinYaml:
 #people = None
  yamld  = None # type: dict[str, Any] # populated from YAML
  yamlFn = None # type: str
  pgzImagesPrefix = "images/"

  ############# load yaml #############

  def loadYaml(self, yamlFn: Optional[str] = None):
    try:
      pif = self.pgzImagesPrefix
      if yamlFn is not None: self.yamlFn = yamlFn
      yamlf      = open(self.yamlFn, 'rt')
      self.yamld = yaml.safe_load(yamlf)
      yamlf.close()

      for abbrev, entry in self.yamld["people"].items():
        abbrevLower = abbrev.lower()
        imgFn = "people/" + abbrevLower
        if not filepatExists(pif+imgFn): self.msg("loadYaml ignoring " + abbrev); continue
        p = self.personClass(imgFn) #single pgz file-specifying argument -> enoActor
        p.loadYamlDict(entry)
        self.addPerson(p)

    except: self.err("loadYaml")

################### Enodia Theme ###################

class EnoThemeMixinYaml:
  name    = None # type: str | None 
  colors  = None # type: ColorRings | None
  themes  = None # type: list[str]  | None

  def loadYamlDict(self, d: dict):
    try:
      self.name    = d.get("name")
      self.themes  = d.get("themes", [])

      # RGB tuples
      if "colors" in d:
        self.colors = {
          k: tuple(v) for k, v in d["colors"].items()
        }

      return self
    except: self.err("loadYamlDict")

################### Enodia Themes ###################

class EnoThemesMixinYaml:
 #themes = None # type: list[EnoTheme]
  yamld  = None # type: dict[str, Any] # populated from YAML
  yamlFn = None # type: str

  def loadYaml(self, yamlFn: Optional[str] = None):
    try:
      if yamlFn is not None: self.yamlFn = yamlFn
      yamlf      = open(self.yamlFn, 'rt')
      self.yamld = yaml.safe_load(yamlf)
      yamlf.close()

      for abbrev, entry in self.yamld["categories"].items():
        t = self.themeClass()
        t.loadYamlDict(entry)
        self.addTheme(t)
    except: self.err("loadYaml")

### end ###
