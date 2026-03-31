# Enodia Media Assets
# Brygg Ullmer, Clemson University and CoPilot
# Begun 2026-03-28

import os
from ataBase import *
from enoRemoteContent import EnoRemoteContent
from enoOSsupport import filepatExists

################### Enodia Media Asset ###################

class EnoMediaAsset(AtaBase):

  mediaSubpath = "images/"
  cacheSubpath = "cache/"
  mediaUrl       = None
  mediaFn        = None
  expectedSha256 = None
  trustPolicy    = None
  allowInsecure  = False
  verbose        = True

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
    super().__init__()

    try:    self.stageMediaForUse()
    except: self.err("__init__")

  ############# stage media for use #############

  def stageMediaForUse(self):
    try:
      msc = self.mediaSubpath + self.cacheSubpath
      os.makedirs(msc, exist_ok=True)

      if self.mediaUrl is None or self.mediaFn is None:
        self.msg("stageMediaForUse: insufficient media specification")
        return False

      mpath = msc + self.mediaFn
      if filepatExists(mpath):
        if self.verbose:
          self.msg("stageMediaForUse: media present, skipping download")
        return True

      erc = EnoRemoteContent(
        url=self.mediaUrl,
        localFn=self.mediaFn,
        expectedSha256=self.expectedSha256,
        trustPolicy=self.trustPolicy,
        allowInsecure=self.allowInsecure
      )
      erc.cacheRoot = self.mediaSubpath + self.cacheSubpath

      return erc.stage()

    except:
      self.err("stageMediaForUse")
      return False

### end ###
