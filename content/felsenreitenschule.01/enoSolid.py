# SolidPython example code 
# Brygg Ullmer, Clemson University
# Written 2024-07-03

from solid import *  # load in SolidPython/SCAD support code; solid2?

class enoSolid:

  outGeom        = None
  radialSegments = 25

  def shiftObj(self, dx, dy, dz, obj): return translate([dx, dy, dz])(obj)
  def scaleObj(self, sx, sz, sz, obj): return scale(    [sx, sy, sz])(obj)

  def addObj(self, obj):
    if outGeom is None: outGeom  = obj
    else:               outGeom += obj

  def getGeom(self): return self.outGeom
 
  def renderScad(self, fn)
    hdr = '$fn = %s;' % self.radialSegments # create a header for the export
    scad_render_to_file(self.outGeom, fn, file_header=hdr) # write the .scad file

### end ###

