# SolidPython example code for illuminated Salzburg Feltenreitenschule
# Brygg Ullmer, Clemson University
# Written 2024-06-24

from solid    import *  # load in SolidPython/SCAD support code; solid2?
from enoSolid import *
      
class enoFRS(enoSolid):

  #dimensions in mm, mating to 144/m LED strip

  elDim = {'arch': [6. , 1.9, 5.], 'dentil': [1.34, .56, 2.5], 
           'box':  [6.4, 4.7, 2.], 'column': [1.,  4.7, None]}

  archGridWH = [10, 5] # width and height (in # arches) of arch grid

  perBoxGeoms  = {}; boxWidth = elDim['box'][0] + elDim['column'][0]

  ########### synthesize a single portal at origin ########### 
  
  def synthPortal(self):

    for elName in ['column', 'dentil']: #create cubical masses for columns and dentils
      w,h,d = self.elDim[elName]; self.perBoxGeoms[elName] = cube([w,h,d])

    aw, ah, ad  = self.elDim['arch']                 # Prep to carve the arch
    archCyl1    = cylinder(r=.5, h=ad)               # We'll excise this cylinder from the archCutter
    archCyl2    = self.scaleObj(aw, ah, 1, archCyl1) # scaling it per elDimensions

    archCutter1 = cube([aw*1.1, ah, ad*.5])          # and borrow the archs dimensions, with less depth
    archCutter2 = self.shiftObj(-aw*1.1/2., 0, .2, archCutter1) #shifting it appropriately, including nudges

    archCutter3 = archCutter2 - archCyl2             # now, Boolean-subtract the cylindrical void 
    archCutter4 = self.shiftObj(0, 1.5, -.3, archCutter3)

    archBox1    = cube([aw, ad, ah])
    archBox2    = self.shiftObj(-aw/2., -ad/2., 0, archBox1)
    archBox3    = archBox2 - archCutter4 
    return archBox3

  ########### synthesize a 2D array of portals at origin ########### 

  def synthPortal2DArray(self, numX, numY):
    
    singlePortal = self.synthPortal()
    rowPortals   = singlePortal
    aw, ah, ad   = self.elDim['arch']                 # Prep to carve the arch

    x1 = 0; dx = aw + self.elDim['column'][0]
    y1 = 0; dy = ah + 4.

    for i in range(numX):
      x1 += dx
      shiftedPortal = self.shiftObj(x1, 0, 0, singlePortal)
      rowPortals   += shiftedPortal

    result = rowPortals
    for i in range(numY):
      y1            += dy
      shiftedPortals = self.shiftObj(0, y1, 0, rowPortals)
      result        += shiftedPortals

    return result

### end ###

