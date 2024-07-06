# SolidPython example code 
# Brygg Ullmer, Clemson University
# Written 2024-07-03

from solid import *  # load in SolidPython/SCAD support code; solid2?
import yaml, traceback

class enoSolid:

  outGeom        = None #output geometry representation
  yamlFn         = None #YAML filename 
  yamlD          = None #YAML data
  yamlParams     = None
  yamlGeomDescr  = None

  radialSegments = 25   #radial segments, used by OpenSCAD for curve transformation
  geomDict       = None #geometries dictionary
  geomNameList   = None

  ######## constructor / class initiation method ######## 

  def __init__(self, **kwargs): 
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.geomDict = {}; self.geomNameList = []

    if self.yamlFn is not None:
      self.loadYaml()

  def err(self, msg): print("enoSolid error:", msg)

  ######## constructor / class initiation method ######## 

  def shiftObj(self, dx, dy, dz, obj): return translate([dx, dy, dz])(obj) #convenience shift  func
  def spinObj(self,  ax, ay, az, obj): return rotate(   [ax, ay, az])(obj) #convenience rotate func
  def scaleObj(self, sx, sy, sz, obj): return scale(    [sx, sy, sz])(obj) #convenience scale  func

  def addObj(self, obj):
    if outGeom is None: outGeom  = obj
    else:               outGeom += obj

  def getGeom(self): return self.outGeom

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
        elif 'op' in geomParams: self.parseYamlGeomOp(geomName, geomParams)
        else:                    err("parseYamlGeomDescr: ignoring unparseable entry:", geomName, geomParams)

  ######## parse yaml geometry type ######## 

  def parseYamlGeomType(self, geomName, geomParams):
    if 'type' not in geomParams: err("parseYamlGeomType: type not found"); return None

    geomType = geomParams['type']

    if geomType == 'portal2DArrayHoles':

    if geomType in self.registeredGeomTypeHandlers:
      try:
        geomTypeHandler = self.registeredGeomTypeHandlers[geomType]
        geomTypeHandler() # likely dangerous; some sandboxing most likely prudent
      except:
        err("parseYamlGeomType: error in extracting+executing geomTypeHandler for", geomType)
        traceback.print_exc(); return None

    else:
      err("parseYamlGeomType: unknown geometry type:", geomType); return None

  ############## render OpenSCAD output ##############
 
  def renderScad(self, fn, outGeomOverride = None):
    hdr = '$fn = %s;' % self.radialSegments # create a header for the export

    if outGeomOverride is None: og = self.outGeom
    else:                       og = outGeomOverride

    scad_render_to_file(og, fn, file_header=hdr) # write the .scad file

### end ###

