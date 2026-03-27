# Experiment in representing a gridded workspace (virtual or physical)
# Brygg Ullmer, Clemson University
# Begun 2026-03-27

from ataBase               import *
from typing                import Any, List

Matrix = List[List[Any]]

class EnoMatrix(AtaBase):
  rows: int|None = None
  cols: int|None = None
  gridWorkspace: Matrix|None = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ################## create matrix  ##################

  def createMatrix(self, rows: int|None=None, cols: int|None=None):
    try:
      if rows is None:
        if self.rows is not None: rows = self.rows
        else: self.msg("createMatrix: rows size not specified!"); return None
      else: self.rows = rows 

      if cols is None:
        if self.cols is not None: cols = self.cols
        else: self.msg("createMatrix: cols size not specified!"); return None
      else: self.cols = cols

      self.gridWorkspace = []
      for col in range(cols)
    
    if 

### end ###
