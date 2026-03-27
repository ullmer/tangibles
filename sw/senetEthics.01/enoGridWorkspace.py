# Experiment in representing a gridded workspace (virtual or physical)
# Brygg Ullmer, Clemson University
# Begun 2026-03-27

from enoSegmentedImgCoords import *
from ataBase               import *
from typing                import Any, List

Matrix = List[List[Any]]

class EnoGridWorkspace(AtaBase):
  width:  int|None = None
  height: int|None = None
  gridWorkspace: Matrix|None         = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ################## create matrix  ##################

  def createMatrix(self, rows: int|None=None, cols: int|None=None):
    if dimensions is Tuple and 
    w, h = 
    if 

### end ###
