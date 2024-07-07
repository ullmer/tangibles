# SolidPython example code 
# Brygg Ullmer, Clemson University
# Written 2024-07-03

from solid    import *  # load in SolidPython/SCAD support code; solid2?
from enoSolid import *
import yaml, traceback

class enoSolidYaml(enoSolid):

  yamlFn         = None #YAML filename 
  yamlD          = None #YAML data
  yamlParams     = None
  yamlGeomDescr  = None

  geomTypeHandler = None
  geomOpHandler   = None

  ######## register handlers ######## 

  def registerTypeHandler(self, typeName, typeParser): self.geomTypeHandler[typeName] = typeParser
  def registerOpHandler(self, opName, opParser):       self.geomOpHandler[opName]     = opParser

  ######## constructor / class initiation method ######## 

  def __init__(self, **kwargs): 
    super().__init__(kwargs)

    self.geomTypeHandler = {}
    self.geomOpHandler   = {}

    if self.yamlFn is not None:
      self.loadYaml()

    self.registerOpHandler('shiftObj', self.parseOpShiftObj)
    self.registerOpHandler('spinObj',, self.parseOpSpinObj)
    self.registerOpHandler('scaleObj', self.parseOpScaleObj)

  ######## error handler (later, to allow non-print error routing) ######## 

  def err(self, msg): print("enoSolidYaml error:", msg)

  ######## geometry operation parsers ######## 

  def parseGeometryOp(self, geomName, geomParams):
    try:
      x           = geomParams['x']  #should be generalized, probably in a YAML file; for now, hardwiring
      y           = geomParams['y']

      if 'lengthShift' in geomParams: lengthShift = geomParams['lengthShift']
      else                          : lengthShift = 0

      if 'wallThickness' in geomParams: wallThickness = geomParams['wallThickness']
      else:                             wallThickness = self.wallThickness

      self.synthPortal2DArrayHoles(x, y, wallThickness, lengthShift)
    except:
      err("parseYamlGeomType: portal2DArrayHoles expects x, y, lengthShift; error:" )
      traceback.print_exc(); return None

  ######## geometry operation parsers ######## 

  def self.parseOpShiftObj(self, opParams): 
    try:
      geomOrig = opParams['geomOrig']
      coords   = opParams['coords']
    except:
      err("parseOpShiftObj: error extracting parameters");
      traceback.print_exc(); return None
      print("MORE TO COME")
      
  ######## load yaml ######## 

  def loadYaml(self):
    if self.yamlFn is None: self.err("loadYaml: yamlFn == None");         return None

    try:    yamlF = open(self.yamlFn, 'rt')
    except: self.err("loadYaml: error opening yamlFn", self.yamlFn);      return None

    try:    self.yamlD = yaml.safe_load(yamlF)
    except: self.err("loadYaml safe_load error:"); traceback.print_exc(); return None

    if 'params'    in self.yamlD: self.yamlParams    = self.yamlD['params']
    if 'geomDescr' in self.yamlD: self.yamlGeomDescr = self.yamlD['geomDescr']

    if self.yamlGeomDescr is not None: self.parseYamlGeomDescr()

  ######## parse yaml geometry description ######## 

  def parseYamlGeomDescr(self): 
    if self.yamlGeomDescr is None:           self.err("parseYamlGeomDescr: yamlGeomDescr is None!");      return None

    if type(self.yamlGeomDescr) is not list: self.err("parseYamlGeomDescr: yamlGeomDescr is not a list"); return None

    for geomDescrEl in self.yamlGeomDescr: #iterate through list
      for geomName in geomDescrEl:
        geomParams = geomDescrEl[geomName]
        self.geomNameList.append(geomName)
        self.geomDict[geomName] = geomParams

        if 'type' in geomParams: self.parseYamlGeomType(geomName, geomParams)
        elif 'op' in geomParams: self.parseYamlGeomOp(  geomName, geomParams)
        else:                    err("parseYamlGeomDescr: ignoring unparseable entry:", geomName, geomParams)

  ######## parse yaml geometry type ######## 

  def parseYamlGeomOp(self, geomName, geomParams):
    if 'op' not in geomParams: err("parseYamlGeomOp: op not found"); return None

    geomOp = geomParams['op']

    if geomType in self.registeredGeomOpHandlers:
      try:
        geomOpHandler = self.registeredGeomOpHandlers[geomOp]
        geomOpHandler(geomName, geomParams) # likely dangerous; some sandboxing most likely prudent
      except:
        err("parseYamlGeomOp: error in extracting+executing geomOpHandler for", geomOp)
        traceback.print_exc(); return None

  #- sideGridL1:   {orig: sideGrid,   op: spinObj,  coords: [  0  0, -90]}
 
  ######## parse yaml geometry type ######## 

  def parseYamlGeomType(self, geomName, geomParams):
    if 'type' not in geomParams: err("parseYamlGeomType: type not found"); return None

    geomType = geomParams['type']

    if geomType in self.registeredGeomTypeHandlers:
      try:
        geomTypeHandler = self.registeredGeomTypeHandlers[geomType]
        geomTypeHandler(geomName, geomParams) # likely dangerous; some sandboxing most likely prudent
      except:
        err("parseYamlGeomType: error in extracting+executing geomTypeHandler for", geomType)
        traceback.print_exc(); return None

    else:
      err("parseYamlGeomType: unknown geometry type:", geomType); return None

### end ###

