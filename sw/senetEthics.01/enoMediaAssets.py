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
        self.downloadMedia(); return True

      if self.mediaFn is not None:
        mediaPath = self.mediaSubpath + 
    if None not in [self.mediaSubpath

    except: self.err("stageMediaForUse")

################### Enodia Media Assets ###################

class EnoMediaAssets(AtaBase):

### end ###
