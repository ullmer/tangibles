# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-06-24

from solid import *  # load in SolidPython/SCAD support code; solid2?
      
#dimensions in mm, mating to 144/m LED strip

elDim = {'arch': [6. , 1.9, 5.], 'dentil': [1.34, .56, 2.5], 
         'box':  [6.4, 4.7, 2.], 'column': [1.,  4.7, None]}

perBoxGeoms  = {}; boxWidth = elDim['box'][0] + elDim['column'][0]

for elName in ['column', 'dentil']: #create cubical masses for columns and dentils
  w,h,d = elDim[elName]; perBoxGeoms[elName] = cube([w,h,d])

aw, ah, ad  = elDim['arch']                # Prep to carve the arch
archCyl1    = cylinder(r=.5, h=ad)         # We'll excise this cylinder from the archCutter
archCyl2    = scale([aw, ah, 1])(archCyl1) # scaling it per elDimensions
archCutter1 = cube([aw, ah, ad*.9])        # and borrow the archs dimensions, with less depth
archCutter2 = translate([0, ah/2., 0])(archCutter1) #shifting it upwards by the radius
archCutter3 = archCutter2 - archCyl2       # now, Boolean-subtract the cylindrical void 

outGeom = archCutter3

print(scad_render(outGeom))

### end ###

