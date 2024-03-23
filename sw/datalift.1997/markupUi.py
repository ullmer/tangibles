# Datalift Markup UI 
# Original by Brygg Ullmer, Jay Lee, and Kerstin Hoeger, May 1998
# Python port by Brygg Ullmer and , Clemson University, June 2022

import picStruct
import picUI
import glob

images = glob.glob("ml-images/*.png")
regsub -all {ml-oimages/} $images {} images

set imageIdx 0
set firstimage [lindex $images 0]

bldgPicUI ui -imageFileName $firstimage -doneCB {nextImage} \
    -imageFilePrefix {ml-oimages/}
ui buildUI

def nextImage():
  global imageIdx, images
  imageIdx += 1

  set image [lindex $images $imageIdx]

  ui delete

  bldgPicUI ui -imageFileName $image -doneCB {nextImage} \
    -imageFilePrefix {ml-oimages/}

  ui buildUI


### end ###
