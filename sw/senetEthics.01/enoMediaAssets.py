# Enodia Backdrops
# Brygg Ullmer, Clemson University
# Begun 2026-03-28

import yaml
from enoOSsupport    import *

################### Enodia Media Asset ###################

class EnoMediaAsset:
  mediaSubpath    = "images/" # type: str|None
  mediaUrl        = None      # type: str|None
  mediaLocalpath  = None      # type: str|None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

### end ###
