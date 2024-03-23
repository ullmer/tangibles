# Building visualization
# Code by Brygg Ullmer, MIT Media Lab
# Begun 12/05/1997

package require pdf::base

############################################################
#################### Class Definitions #####################
############################################################

##################### Floor structure ######################

itcl_class floorStruct {
  inherit pdfBase

## Local methods
  constructor {config} {}

  method assertIv {} {}

## Local members

  public parentIvName {}
  public ivName       {}
  public ivAsserted {0}

  public level  {0} ;# Floor level
  public height {0} ;# Floor altitude, in meters
#  public heightMult {3.5} ;# To exaggerate height for greater legibility
  public heightMult {6.5} ;# To exaggerate height for greater legibility

  public xdim   {1} ;#dimensions in meters
  public ydim   {1}

  public relxdim   {1} ;#dimensions which appear in floor data file
  public relydim   {1} ;# (often realspace dims from bldg drawing)

  public imageFile {}  ;#filepath of RGB floor image file
}

##################### Building Vis ######################

itcl_class bldgVis {
  inherit pdfBase

## Local methods
  constructor {config} {}
  method assertIv {} {}

## Local members

  public ivName    {}
  public ivAsserted {0}

  public floorList {}
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
 
  #puts "should assert <<$xivgeom>> here"

  addNObj  $ivName $xivgeom
  moveNObj $ivName:trans [list 0 0 $hval]
  set ivAsserted 1 

  bindNObj $ivName "puts \"This is $ivName\""

  #puts "double check:\n[getNObj $ivName]"
}
 
### END ###
 
