# Experiment in representing a gridded workspace (virtual or physical)
# Brygg Ullmer, Clemson University
# Begun 2026-03-27

from enoSegmentedImgCoords import *
from ataBase               import *
from typing                import Any, List

Matrix = List[List[Any]]

class EnoGridWorkspace(AtaBase):
  dimensions:    tuple[int,int]|None = None
  gridWorkspace: Matrix|None         = None

### end ###
