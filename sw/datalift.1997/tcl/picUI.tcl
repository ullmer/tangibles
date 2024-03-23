# Code for building picture structures supporting IDW P4
# By Brygg Ullmer, MIT Media Lab
# 05/09/1998: Begun

package require pdf::base

##################################################################
#################### building Picture class ######################
##################################################################

itcl_class bldgPicUI {
  inherit bldgPicStruct

  constructor {config} {set structFileName $imageFileName}

  method buildUI   {} {}
  method destroyUI {} {}

  method loadFloorImages {} {}

  method changeFloorUI  {newFloor}  {}
  method changeYearUI   {newYear}   {}
  method changeAspectUI {newAspect} {}

  method updateFloorTarget {x y} {}
  method synthFloorTarget {}    {}

  method mapCanv2Norm {x y} {}
  method mapNorm2Canv {x y} {}

  method evalDoneCB {} {}

 ## local members
  
  public uiBuilt {0}
  public floorCanvas {}
  public lastTargetPos {}
  public doneCB {}
}

#################################################################
################## building Picture UI body #####################
#################################################################
  
#################### load floor images ######################

body bldgPicUI::loadFloorImages {} {
  if {[lsearch [image names] {floor1}] != -1} {return} ;# images loaded
  
  ;# load images
  foreach floor {basement floor1 floor2 floor3 floor4} {
    set filename "images/$floor.gif"
    image create photo $floor -file $filename
  }
}
  
#################### destroy UI ######################

body bldgPicUI::destroyUI {} {
 if {$uiBuilt == 0} {puts "$this destroyUI: claiming not built"; return}

 destroy .controls .floor
 set uiBuilt 0
}

#################### build UI ######################

body bldgPicUI::buildUI {} {

  if {$uiBuilt} {destroyUI} ;# for simplicity, always build UI from scratch

  if {[structExists]} {loadStruct}

 ## Do the basics

  loadFloorImages

  frame  .controls
  canvas .floor
  pack  .controls .floor -side left -fill both

  set floorCanvas .floor
  bind .floor <Button-1> "$this updateFloorTarget %x %y"

  ### Build Controls

  ## Build base controls

  set f .controls
  label $f.file -text "Filename: $imageFileName"

  if {[lsearch [image names] $imageFileName] == -1} { ;# load picture
    set impath [format {%s/%s} $imageFilePrefix $imageFileName]
    regsub {.rgb} $impath {.gif} impath
    if {![file exists $impath]} {puts "$this buildUI error $impath (1)"; return}

    image create photo $imageFileName -file $impath
  }

  label $f.image -image $imageFileName

  ## Build floor controls

  frame $f.floor
  label $f.floor.label -text "Floor: "; pack $f.floor.label -side left
  foreach floor $floorOptions {
    radiobutton $f.floor.$floor -text $floor -variable GzeFloor \
      -command "$this changeFloorUI \$GzeFloor" -value $floor
    pack $f.floor.$floor -side left
  }

  $f.floor.$whichFloor select
  changeFloorUI $whichFloor 
  synthFloorTarget 

  ## Build year controls

  frame $f.year
  label $f.year.label -text "Year: "; pack $f.year.label -side left
  foreach year $yearOptions {
    radiobutton $f.year.$year -text $year -variable GzeYear \
      -command "$this changeYearUI \$GzeYear" -value $year
    pack $f.year.$year -side left
  }

  $f.year.$whichYear select
  changeYearUI $whichYear 

  ## Build aspect controls

  frame $f.aspect
  label $f.aspect.label -text "Aspect: "; pack $f.aspect.label -side left
  foreach aspect $aspectOptions {
    radiobutton $f.aspect.$aspect -text $aspect -variable GzeAspect \
      -command "$this changeAspectUI \$GzeAspect" -value $aspect
    pack $f.aspect.$aspect -side left
  }

  $f.aspect.$imageAspect select
  changeAspectUI $imageAspect

  ## Done...

  button $f.save -text Save -command "$this saveStruct"
  button $f.done -text Done \
    -command "$this saveStruct; $this destroyUI; $this evalDoneCB"
 
  ## Pack the pieces

  pack $f.file $f.image $f.floor $f.year $f.aspect $f.save $f.done -side top
  set uiBuilt 1
}

#################### change Floor ######################

body bldgPicUI::changeFloorUI {newFloor} {

  puts "changing floor to $newFloor"

  set whichFloor $newFloor

  $floorCanvas delete floor

  set width  [image width $newFloor]
  set height [image height $newFloor]

  $floorCanvas configure -width $width -height $height

  set x [expr $width / 2.]
  set y [expr $height / 2.]

  $floorCanvas create image $x $y -image $newFloor -tag floor
  $floorCanvas lower floor
}

#################### change Year ######################

body bldgPicUI::changeYearUI   {newYear}   {
  set whichYear $newYear
}

#################### change Aspect ######################

body bldgPicUI::changeAspectUI {newAspect}   {

  set imageAspect $newAspect

  set t $paneHeight
  set paneHeight $paneWidth
  set paneWidth $t
}

#################### place Floor Target ######################

body bldgPicUI::updateFloorTarget {x y} {

  set ox [lindex $lastTargetPos 0]
  set oy [lindex $lastTargetPos 1]

  set dx [expr $x - $ox]
  set dy [expr $y - $oy]

  $floorCanvas move target $dx $dy

 #Update stored coords

  set npos [mapCanv2Norm $x $y]
  set nx [lindex $npos 0]
  set ny [lindex $npos 1]
  set floorCoord [list $nx $ny]

  puts "npos $npos / $floorCoord"

  set lastTargetPos [list $x $y]
}

#################### synth Floor Target ######################

body bldgPicUI::synthFloorTarget {}    {

  if {$floorCanvas == {}} {
    puts "$this synthFloorTarget: canv not built"; return {}
  }

  set r [$floorCanvas gettags target]
  if {$r != {}} {updateFloorTarget} ;# target already exists

  set nx [lindex $floorCoord 0]
  set ny [lindex $floorCoord 1]

  set cpos [mapNorm2Canv $nx $ny]
  set cx [lindex $cpos 0]
  set cy [lindex $cpos 1]

  set x1 [expr $cx - 7]; set x2 [expr $cx + 7]
  set y1 [expr $cy - 7]; set y2 [expr $cy + 7]

  $floorCanvas create oval $x1 $y1 $x2 $y2 -fill red -tag target

  set lastTargetPos [list $cx $cy]
}

#################### map Canvas 2 Normal ######################

body bldgPicUI::mapCanv2Norm {x y} {
  set cwidth  [image width $whichFloor]
  set cheight [image height $whichFloor]

  set rx [expr $x / double($cwidth)]
  set ry [expr $y / double($cheight)] 

  set result [list $rx $ry]

  puts "map $x $y / $whichFloor $cwidth $cheight / $rx $ry"
  return $result
}

#################### map Normal 2 Canvas ######################

body bldgPicUI::mapNorm2Canv {x y} {
  set cwidth  [image width $whichFloor]
  set cheight [image height $whichFloor]

  set rx [expr $cwidth  * double($x)]
  set ry [expr $cheight * double($y)]

  set result [list $rx $ry]
  return $result
}

#################### map Normal 2 Canvas ######################

body bldgPicUI::evalDoneCB {} {

  set errcode [catch {eval $doneCB}]
  if {$errcode} {
    puts "$this evalDoneCB:  error in doneCB eval"
    return
  }
}

## END ##

