# Enodia Media Assets
# Brygg Ullmer, Clemson University
# Begun 2026-03-28

import yaml

from ataBase         import *
from enoOSsupport    import *

# def filepatExists(filepath: str) 
# def downloadRemote(url: str, localPath: str)

################### Enodia Media Asset ###################

class EnoMediaAsset(AtaBase):
  mediaSubpath = "images/" # type: str|None
  mediaUrl     = None      # type: str|None
  mediaFn      = None      # type: str|None
  autoDLMedia  = True      # type: bool

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    try:    self.stageMediaForUse()
    except: self.err("__init__")

  ############# stage media for use #############

  def stageMediaForUse(self):
    try:
      if self.mediaUrl is not None and self.autoDLMedia:
        result = self.downloadMedia(); return result

      if self.mediaFn is not None:
        mediaPath = self.mediaSubpath + self.mediaFn
        if filepatExists(mediaPath): return True
      return False
    except: self.err("stageMediaForUse")

################### Enodia Media Assets ###################

class EnoMediaAssets(AtaBase):
  mediaSubpath = "images/" # type: str|None
  yamlFn = "yaml/mediaAssets"
  yamlD  = None # type: dict[Any]|None
  autoDLMedia  = True      # type: bool

  mediaTypes     = None # type: dict[Any]|None
  mediaTypesStrs = ['backdrops', 'people'] # type: dict[str]

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    try:
      self.loadYaml()
      self.stageMediaForUse()
    except: self.err("__init__")

  ############# load yaml #############

  def loadYaml(self):
    try:
      if not filepatExists(self.yamlFn): 
        self.msg("loadYaml: called, but yaml file doesn't exist"); return False

      yf = open(self.yamlFn, 'rt')
      self.yamlD = yaml.safe_load(yf)
      yf.close()
      return True
    except: self.err("loadYaml")
    return False

  ############# stage media for use #############

  def stageMediaForUse(self):
    try:
      if self.yamlD is None: self.loadYaml()
      if self.autoDLMedia:
        mts = self.mediaTypesStrs
        self.mediaTypes = {}

        for mt in mts:
          if mt not in self.yamlD: 
            self.msg("stageMediaForUse: media type not found in yaml: " + mt); continue
          mty = self.mediaTypes[mt] = self.yamlD[mt]

          for ydt in mty: #yd = yaml data tag

            url = None
            yd  = mty[ydt]

            subpath = self.mediaSubpath + mt + "/"
            if 'local' in yd: mediaFn = yd['local']
            if 'url'   in yd: url     = yd['url']
            ema = EnoMediaAsset(url=url, mediaFn=mediaFn, mediaSubpath=subpath)
            self.mediaTypes[mt][ydt] = ema

    except: self.err("stageMediaForUse")

### end ###

