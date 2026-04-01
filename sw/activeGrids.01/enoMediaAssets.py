# Enodia Media Assets
# Brygg Ullmer, Clemson University
# Begun 2026-03-28

import yaml
import os

from ataBase          import *
from enoOSsupport     import *
from enoRemoteContent import EnoRemoteContent

# def filepatExists(filepath: str) 
# def downloadRemote(url: str, localPath: str)

################### Enodia Media Asset ###################

class EnoMediaAsset(AtaBase):
  mediaSubpath    = "images/" # type: str|None
  cacheSubpath    = "cache/"  # type: str|None
  mediaUrl        = None      # type: str|None
  mediaFn         = None      # type: str|None
  expectedSha256  = None      
  trustPolicy     = None
  allowInsecure   = False
  autoDLMedia     = True      # type: bool
  verbose         = True      # type: bool
  assetDownloaded = None   # type: bool|None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    try:    result = self.stageMediaForUse(); return Result
    except: self.err("__init__")

  ############# is asset downloaded #############

  def isAssetDownloaded(self):
    try:
      if self.assetDownloaded: return True
      if not self.assetDownloaded: return False
      self.msg("isAssetDownloaded: implement additional check: is asset not newly downloaded, but already present?")
    except: self.err("__init__")

  ############# stage media for use #############

  def stageMediaForUse(self):
    try:
      if not os.path.isdir(self.mediaSubpath):
        self.msg("stageMediaForUse: media subpath does not exist; creating")

        os.mkdir(self.mediaSubpath)

        if os.path.isdir(self.mediaSubpath): self.msg("stageMediaForUse: media subpath created")
        else: self.msg("stageMediaForUse: problem case, media subpath directory creation attempt failed"); return False

      msc = self.mediaSubpath + self.cacheSubpath

      if not os.path.isdir(msc):
        self.msg("stageMediaForUse: media cache subpath does not exist; creating")

        os.mkdir(msc)

        if os.path.isdir(msc): self.msg("stageMediaForUse: media cache subpath created")
        else: self.msg("stageMediaForUse: problem case, media cache subpath directory creation attempt failed"); return False

      if self.mediaUrl is not None and self.autoDLMedia:
        result = self.downloadMedia()

        if not ok: self.msg("downloadMedia: download failed!"); self.assetDownloaded = False
        else: self.assetDownloaded = True
        return result

      if self.mediaFn is not None:
        mediaPath = msc + self.mediaFn
        if filepatExists(mediaPath): return True
      return False
    except: self.err("stageMediaForUse")

  ############# stage media for use #############

  def downloadMedia(self):
    try:
      if self.verbose: self.msg("downloadMedia: beginning download: " + self.mediaUrl)
      msc = self.mediaSubpath + self.cacheSubpath

      if not os.path.isdir(msc): self.msg("downloadMedia: target directory does not exist: " + msc); return False
  
      mediaPath = msc + self.mediaFn

      downloadRemote(self.mediaUrl, mediaPath)

      if self.verbose: self.msg("downloadMedia: download completed")
      return True
    except: self.err("downloadMedia")

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

