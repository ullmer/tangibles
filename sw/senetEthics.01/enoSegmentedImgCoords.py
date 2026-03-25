# Map YAML description of segmented image to segment centroid vertices
# Brygg Ullmer (Clemson University) and CoPilot
# Begun 2026-03-24

import numpy as np

def lerp(a, b, t): return a * (1 - t) + b * t

def imgGrid2coord(x, y, data):
  # Extract components
  TL, TR, BL, BR = map(lambda p: np.array(p, dtype=float), data["coords"])
  tTop    = np.array(data["sectorIndices"]["top"])
  tBottom = np.array(data["sectorIndices"]["bottom"])
  tLeft   = np.array(data["sectorIndices"]["left"])
  tRight  = np.array(data["sectorIndices"]["right"])

  # Mid-fractions for the cell's center
  tTopMid    = 0.5*(tTop[x]  + tTop[x+1])
  tBottomMid = 0.5*(tBottom[x] + tBottom[x+1])
  tLeftMid   = 0.5*(tLeft[y]   + tLeft[y+1])
  tRightMid  = 0.5*(tRight[y]  + tRight[y+1])

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

### end ###
