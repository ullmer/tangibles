# Simple 2D Matrix
# Brygg Ullmer, Clemson University
# Begun 2026-03-27

# Using pandas or numpy might have made sense, but considering a variant either in
# micropython or a micropython c binding, and special aspects re subclass warping

from ataBase               import *
from typing                import Any, List

Matrix = List[List[Any]]

class EnoMatrix2D(AtaBase):
  rows:   int|None = None
  cols:   int|None = None
  matrix: Matrix|None = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ################## getSize ##################

  def getSize(self):
    try:    result = (rows, cols); return result
    except: self.err("getSize")

  ################## validIndices ##################
  def validIndices(self, i: int, j: int):
    try:    
      if not isinstance(i, int): self.msg("checkBounds: i not integer!"); return False
      if not isinstance(j, int): self.msg("checkBounds: j not integer!"); return False

      if i < 0 or i > self.cols: self.msg("checkBounds: i out of bound!"); return False
      if j < 0 or j > self.rows: self.msg("checkBounds: j out of bound!"); return False
      return True

  ################## getEl ##################

  def getEl(self, i: int, j: int):
    try:    
      if not self.validIndices(i, j): self.msg("getEl: invalid indices"); return None
      result = self.matrix[i][j]
      return result
    except: self.err("getEl")

  ################## setEl ##################

  def setEl(self, i: int, j: int, val: Any):
    try:    
      if not self.validIndices(i, j): self.msg("setEl: invalid indices"); return None
      self.matrix[i][j] = val
      return True
    except: self.err("getEl"); return False

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

      self.matrix = []
      for col in range(cols):
        el = [None]*rows
        self.matrix.append(el)

      return True
    except: self.err("createMatrix")
    
### end ###
