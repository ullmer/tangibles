from solid import *
from solid.utils import *

def extrudedText(txt, height=.006, font_size=.012):
  t1 = text(txt, size=font_size, halign='center', valign='center')
  t2 = linear_extrude(height)(t1)
  return t2

if __name__ == '__main__':
  txt     = "hello world"
  stlFn   = "enodiaNfcTok01a.stl"
  extr1   = extrudedText(txt)
  stl1    = import_stl(stlFn)
  outGeom = stl1 + extr1
  #outGeom = stl1 

  scad_render_to_file(outGeom, 'stxt02.scad')

### end ###
