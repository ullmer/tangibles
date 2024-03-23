source picStruct.tcl
source picUI.tcl

set images [glob ml-oimages/*.rgb]
#set images [glob ml-images/*.rgb]
#set images [glob ml-images/*75.rgb]

regsub -all {ml-oimages/} $images {} images

set imageIdx 0

set firstimage [lindex $images 0]

bldgPicUI ui -imageFileName $firstimage -doneCB {nextImage} \
    -imageFilePrefix {ml-oimages/}
ui buildUI


proc nextImage {} {
  global imageIdx images
  incr imageIdx

  set image [lindex $images $imageIdx]

  ui delete

  bldgPicUI ui -imageFileName $image -doneCB {nextImage} \
    -imageFilePrefix {ml-oimages/}

  ui buildUI
}


