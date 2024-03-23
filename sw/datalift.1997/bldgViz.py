# Building visualization
# Code by Brygg Ullmer, MIT Media Lab & Clemson University
# Begun 12/05/1997
# Python port begun 2022-06-29


############################################################
#################### Class Definitions #####################
############################################################

##################### Floor structure ######################

class floorStruct:

## Local fields

  parentIvName  = None
  ivName        = None
  ivAsserted    = 0
  level         = 0   # Floor level
  height        = 0   # Floor altitude, in meters
  heightMult    = 6.5 # To exaggerate height for greater legibility

  xdim          = 1 #dimensions in meters
  ydim          = 1

  relxdim       = 1 #dimensions which appear in floor data file
  relydim       = 1 # (often realspace dims from bldg drawing)

  imageFile     = None #filepath of RGB floor image file

##################### Building Vis ######################

class bldgViz:

## Local fields

  ivName     = None
  ivAsserted = 0
  floorList  = None
}

################################################################
########################## Building Vis ########################
################################################################

######################## constructor #######################

body bldgVis::constructor {config} {
  regsub {^.*::([^:].*)$} $this {\1} ivName
}

######################## constructor #######################

body bldgVis::assertIv {} {

  addNFrame $ivName
  puts "building vis for floors $floorList"

  foreach floor $floorList {
    puts "Building vis for floor $floor"
    $floor config -parentIvName $ivName
    $floor assertIv
  }

  set ivAsserted 1
}

################################################################
######################## Floor Structure #######################
################################################################

######################## constructor #######################

body floorStruct::constructor {config} {
  regsub {^.*::([^:].*)$} $this {\1} tempIvName

  if {$parentIvName == {}} {set ivName $tempIvName; return}

  set ivName [format {%s:%s} $parentIvName $tempIvName]
}

######################## assertIv #######################

body floorStruct::assertIv {} {

  set hx [expr $xdim / 2.] 
  set hy [expr $ydim / 2.]
  set hval [expr $height * $heightMult] 

#    Coordinate3 {point [0 $ydim 0, $xdim $ydim 0, $xdim 0 0, 
#       0 0 0, 0 $ydim 0]}

  set ivgeom {
    #DEF $ivName:transp Material {transparency .5}
    DEF $ivName:transp Material {transparency .3}
    TextureCoordinate2 {point [0 1, 1 1, 1 0, 0 0]}
    Texture2 {filename "$imageFile" model DECAL}
    NormalBinding {value PER_FACE}
    Normal {vector 0 1 0}
    Coordinate3 {point [-$hx $hy 0, $hx $hy 0, $hx -$hy 0, 
       -$hx -$hy 0, -$hx $hy 0]}
    FaceSet {numVertices 4}
  }
 
  set xivgeom [subst -nocommands $ivgeom]
 
  addNObj  $ivName $xivgeom
  moveNObj $ivName:trans [list 0 0 $hval]
  set ivAsserted 1 

  bindNObj $ivName "puts \"This is $ivName\""

  #puts "double check:\n[getNObj $ivName]"
}
 
### END ###
 
