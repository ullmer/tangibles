from solid import *
from solid.utils import *

def extrudedText(txt, height=10, font_size=12, thickness=2):
  t1 = text(txt, size=font_size, halign='center', valign='center')
  t2 = linear_extrude(height)(t1)
  return t2

if __name__ == '__main__':
  txt = "greetings"
  extruded = extrudedText(txt)
  scad_render_to_file(extruded, 'stxt01.scad')

### end ###
