# Non-uniform grid support
# Brygg Ullmer, Clemson University
# Begun 2025-03-19

import glob, math, yaml, traceback

from enoCoordFuncs import *

#################### non-uniform grid ####################

class enoNUGrid:

  baseName           = None
  yamlD              = None
  numDivsX, numDivsY = 7, 12

  cornerCoords         = None
  leftDivs,  rightDivs = None, None
  topDivs,  bottomDivs = None, None
  divsEnsemble         = None
  divSectors           = ["top", "bottom", "right", "left"]

  leftVertices, rightVertices, topVertices, bottomVertices = [None] * 4
  sideVertexHandles  = None

  defaultCornerCoords = [(10, 10), (1800, 10), (10, 1000), (1800, 1000)]
  verbose             = True

  #################### constructor ####################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

    self.initFieldVars()
    if self.cornerCoords is None: self.setDefaultCoords()

  #################### get/set corner coordinate ####################

  def getCornerCoord(self, idx):
    try:    return self.cornerCoords[idx]
    except: self.err("getCornerCoord error"); return None

  def setCornerCoord(self, idx, coordVal):
    try:    self.cornerCoords[idx] = coordVal
    except: self.err("setCornerCoord error"); return None

  #################### constructor ####################

  def initFieldVars(self):
    self.leftVertices, self.rightVertices  = {}, {}
    self.topVertices,  self.bottomVertices = {}, {}
    self.sideVertexHandles = {}
    self.sideVertexHandles['left']   = self.leftVertices #unsure if this is the best approach; trying it out
    self.sideVertexHandles['right']  = self.rightVertices
    self.sideVertexHandles['top']    = self.topVertices
    self.sideVertexHandles['bottom'] = self.bottomVertices

    self.leftDivs,  self.rightDivs = [], []
    self.topDivs,  self.bottomDivs = [], []

    self.divsEnsemble = {}
    self.divsEnsemble['left']   = self.leftDivs
    self.divsEnsemble['right']  = self.rightDivs
    self.divsEnsemble['top']    = self.topDivs
    self.divsEnsemble['bottom'] = self.bottomDivs

  #################### message ####################

  def msg(self, msgStr): print("enoNUGrid msg: " + str(msgStr))
  def err(self, msgStr): print("enoNUGrid err: " + str(msgStr)); traceback.print_exc()

  #################### genFloatListStr ####################

  def genFloatListStr(self, floatList):
    result = []
    for fval in floatList: valstr = f"{fval:.3f}"; result.append(valstr)
  
    resultStr = "[" + ", ".join(result) + "]"
    return resultStr
  
  #################### coordinates: tuples to lists #################### 

  def coordsTuplesToLists(self, ctuples):
    result = []
    for tuple in ctuples:
      a, b = tuple
      result.append([a,b])
    return result

  #################### coordinates: tuples to lists #################### 

  def coordsListsToTuples(self, clists):
    result = []
    for cl in clists:
      a, b = cl
      result.append((a,b))
    return result

  #################### genYaml ####################

  def genYaml(self):
    result = ''
    c = self.coordsTuplesToLists(self.cornerCoords)

    ndx, ndy = self.numDivsX, self.numDivsY
    result += "  numDivs: [%i, %i]\n" % (ndx, ndy)
    result += "  coords:  " + str(c) + "\n"
    result += "  sectorIndices:\n"
    for sector in self.divSectors:
      divIndices = self.divsEnsemble[sector]
      fls = self.genFloatListStr(divIndices)
      result += "    " + sector + ": " + str(fls) + "\n"

    return result

  def printYaml(self):
    yamlstr = self.genYaml()
    print(yamlstr)

  #################### populateViaSourceDict ####################
  # parses a source dictionary, as yielded by parsing of genYaml 

  def populateViaSourceDict(self, sourceDict):
    necessaryFields = ["numDivs", "coords", "sectorIndices"]
    for nf in necessaryFields:
      if nf not in sourceDict: 
        self.msg("populateViaSourceDict missing necessary field", nf)
        return None

    si = sourceDict["sectorIndices"]
    for ds in self.divSectors:
      if ds not in si:
        self.msg("populateViaSourceDict missing necessary divsector", ds)
        return None

    self.numDivsX, self.numDivsY = sourceDict["numDivs"]
    coords = sourceDict["coords"]
    self.cornerCoords = self.coordsListsToTuples(coords)

    for ds in self.divSectors:
      de = self.divsEnsemble[ds] # we need to copy over entries from sourceDict 
      de.clear()
      for val in si[ds]: de.append(val)

  #################### save yaml ####################

  def saveYaml(self):
    self.msg("saveYaml called")
    if self.baseName is not None:
      yfn = self.baseName + '.yaml'
      f  = open(yfn, 'wt')
    else: self.msg("saveYaml problem: baseName not defined"); return

    yamlStr = self.genYaml()
    f.write(self.baseName + ':\n')
    f.write(yamlStr)
    f.close()

  #################### load yaml ####################

  def loadYaml(self):
    self.msg("loadYaml called")
    if self.baseName is not None:
      yfn = self.baseName + '.yaml'
      yf  = open(yfn, 'rt')
    else: self.msg("loadYaml problem: baseName not defined"); return

    self.yamlD = yaml.safe_load(yf)
    yf.close()

    if self.baseName not in self.yamlD:
      self.msg("loadYaml error: baseName not found in yaml file:" + self.baseName)
      return None

    sourceDict = self.yamlD[self.baseName]
    self.populateViaSourceDict(sourceDict)
 
  #################### draw ####################

  def setDefaultCoords(self):
   self.cornerCoords = []

   for cc in self.defaultCornerCoords: self.cornerCoords.append(cc)
   self.calcDefaultXYdivs()

  #################### calculate default x/y divisions ####################

  def calcDefaultXYdivs(self):

   dx = 1./float(self.numDivsX); xi = 0 #by default, set evenly
   dy = 1./float(self.numDivsY); yi = 0 #by default, set evenly

   for i in range(self.numDivsX+1): 
     self.topDivs.append(xi); self.bottomDivs.append(xi); xi += dx

   for i in range(self.numDivsY+1): 
     self.leftDivs.append(yi); self.rightDivs.append(yi); yi += dy

  #################### interpolate coordinate ####################

  def interpolateCoord(self, a, b, p):
    x1, y1 = a; x2, y2 = b
    x = x1 + p * (x2 - x1)
    y = y1 + p * (y2 - y1)
    return (x, y)
  
  #################### get x division coordinates ####################

  def getXDivCoords(self, idx): 
    try:
      c1, c2, c3, c4 = self.cornerCoords
      if idx >= len(self.topDivs):    self.msg("getXDivCoords: top index too large: " + str(idx)); return None
      if idx >= len(self.bottomDivs): self.msg("getXDivCoords: bottom index too large: " + str(idx)); return None

      xd1, xd2       = self.topDivs[idx], self.bottomDivs[idx]
      xdc1   = self.interpolateCoord(c1, c2, xd1)
      xdc2   = self.interpolateCoord(c3, c4, xd2)
      return [xdc1, xdc2]
    except: self.err("getXDivCoords"); return None

  #################### get y division coordinates ####################

  def getYDivCoords(self, idx): 
    try:
      c1, c2, c3, c4 = self.cornerCoords
      yd1, yd2       = self.leftDivs[idx], self.rightDivs[idx]
      ydc1   = self.interpolateCoord(c1, c3, yd1)
      ydc2   = self.interpolateCoord(c2, c4, yd2)

      return [ydc1, ydc2]
    except: self.err("getYDivCoords"); return None

  #################### interpolate coordinate ####################

  def getSectorCoords(self, x, y): 
    try:
      xl1 = self.getXDivCoords(y); xl2 = self.getXDivCoords(y+1)
      yl1 = self.getYDivCoords(x); yl2 = self.getYDivCoords(x+1)

      v1 = getLineIntersection2(xl1, yl1); v2 = getLineIntersection2(xl2, yl1)
      v3 = getLineIntersection2(xl2, yl2); v4 = getLineIntersection2(xl1, yl2)
      result = [v1, v2, v3, v4]
      return result

    except: self.err("getSectorCoords"); return None

### end ###
