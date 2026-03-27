# Map YAML description of segmented image to segment centroid vertices
# Brygg Ullmer (Clemson University) and CoPilot
# Begun 2026-03-24

import numpy as np
from ataBase import *

class EnoSegmentedImgCoords(AtaBase):

  yamlFn  =None
  yamlD   = None
  tTop    = None
  tBottom = None
  tLeft   = None
  tRight  = None

  ############# constructor #############
  def __init__(self, **kwargs): 
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    if self.yamlFn is not None: self.loadYaml()

  ############# lerp #############

  def loadYaml(self):
    try:
      if self.yamlFn is None: self.msg("yamlFn is not initiated"); return None
     
    except: self.err("loadYaml")

  ############# lerp #############

  def lerp(self, a, b, t): return a * (1 - t) + b * t

  ############# image grid to coordinate #############
  
  def imgGrid2Coord(self, x, y):
    try:
      data = self.yamlD
      # Extract components
      TL, TR, BL, BR = map(lambda p: np.array(p, dtype=float), data["coords"])

      if None in [self.tTop, self.tBottom, self.tLeft, self.tRight]:      
        self.tTop    = np.array(data["sectorIndices"]["top"])
        self.tBottom = np.array(data["sectorIndices"]["bottom"])
        self.tLeft   = np.array(data["sectorIndices"]["left"])
        self.tRight  = np.array(data["sectorIndices"]["right"])

      tTop, tBottom, tLeft, tRight = self.tTop, self.tBottom, self.tLeft, self.tRight
    
      # Mid-fractions for the cell's center
      tTopMid    = 0.5*(tTop[   x] + tTop[   x+1])
      tBottomMid = 0.5*(tBottom[x] + tBottom[x+1])
      tLeftMid   = 0.5*(tLeft[  y] + tLeft[  y+1])
      tRightMid  = 0.5*(tRight[ y] + tRight[ y+1])
    
      # Convert to unified horizontal/vertical fractions
      tx = 0.5*(tTopMid + tBottomMid)
      ty = 0.5*(tLeftMid + tRightMid)
    
      # Bilinear interpolation of a quadrilateral
      center = (
        TL*(1-tx)*(1-ty) +
        TR*(tx)*(1-ty) +
        BL*(1-tx)*ty +
        BR*(tx)*ty
      )
    
      return tuple(center)
    except: self.err("imgGrid2Coord");

### end ###
