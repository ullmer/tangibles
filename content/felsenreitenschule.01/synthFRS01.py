# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-06-24

from solid import *  # load in SolidPython/SCAD support code; solid2?
      
#dimensions in mm, mating to 144/m LED strip

elDim = {'arch': [6. , 1.9, 3.], 'dentil': [1.34, .56, 2.5], 
         'box':  [6.4, 4.7, 2.], 'column': [1., 4.7,      ]}

perBoxGeoms  = {}; boxWidth = elDim['box'][0] + elDim['column'][0]

for elName in ['column', 'dentil']: #create cubical masses for columns and dentils
  w,h,d = elDim[elName]; perBoxGeoms[elName] = cube(w,h,d)

# Next, 
cyl1 = cylinder



c1 = cube()
c2 = translate([1.5, 0, 0])(c1)
outGeom = c1 + c2

print(scad_render(outGeom))

### end ###

