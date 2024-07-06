# SolidPython example code 
# Brygg Ullmer, Clemson University
# Written 2024-07-03

from solid import *  # load in SolidPython/SCAD support code; solid2?

class enoSolid:

  outGeom        = None #output geometry representation
  yamlFn         = None #YAML filename 
  radialSegments = 25   #radial segments, used by OpenSCAD for curve transformation
  geomDict       = None #geometries dictionary

  ######## constructor / class initiation method ######## 

  def __init__(self, **kwargs): #all
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.geomDict = {}

    if self.yamlFn is not None:
      self.loadYaml()

  ######## constructor / class initiation method ######## 

  def shiftObj(self, dx, dy, dz, obj): return translate([dx, dy, dz])(obj) #convenience shift  func
  def spinObj(self,  ax, ay, az, obj): return rotate(   [ax, ay, az])(obj) #convenience rotate func
  def scaleObj(self, sx, sy, sz, obj): return scale(    [sx, sy, sz])(obj) #convenience scale  func

  def addObj(self, obj):
    if outGeom is None: outGeom  = obj
    else:               outGeom += obj

  def getGeom(self): return self.outGeom

  ############## render OpenSCAD output ##############
 
  def renderScad(self, fn, outGeomOverride = None):
    hdr = '$fn = %s;' % self.radialSegments # create a header for the export

    if outGeomOverride is None: og = self.outGeom
    else:                       og = outGeomOverride

    scad_render_to_file(og, fn, file_header=hdr) # write the .scad file

### end ###

