# Enodia Media Assets
# Brygg Ullmer, Clemson University
# Begun 2026-03-28

import yaml

from ataBase         import *
from enoOSsupport    import *

################### Enodia Media Asset ###################

class EnoMediaAsset(AtaBase):
  mediaSubpath    = "images/" # type: str|None
  mediaUrl        = None      # type: str|None
  mediaLocalpath  = None      # type: str|None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

################### Enodia Media Assets ###################

class EnoMediaAssets(AtaBase):

### end ###
