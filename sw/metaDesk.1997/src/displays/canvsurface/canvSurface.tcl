# Tk Canvas surface support routines for metaDESK
# Brygg Ullmer, MIT Media Lab TMG
# Begun 01/01/1997

package require Itcl
package require Tk
package require tmg::base

package provide tmg::canvsurface 1.0

####################   Canvas World  ####################

itcl_class CanvasSurfBase { ;# Canvas base surface

 inherit base

 constructor {config} {
    set members [concat $members $local_members]
 }

### Member functions

  method init {} {
    canvas $canvas -width $rx -height $ry
    pack $canvas

    set ry [expr $ry * $ycorrection]
  }

### Wrl2Canv coord space conversions

  method vertxWrl2Canv {ix} {
    set x [expr 1.0 * ($ix / $vx) * $rx] ;# handle scaling
    return $x
  }

  method vertyWrl2Canv {iy} {
    set y [expr 1.0 * ($iy / $vy) * $ry] ;# handle scaling
    set y [expr $ry - $y]
    return $y
  }

  method vertWrl2Canv {vertex} {
    set ix [lindex $vertex 0]
    set iy [lindex $vertex 1]

    set result [list [vertxWrl2Canv $ix] [vertyWrl2Canv $iy]]
    return $result
  }

  method widthWrl2Canv {ix}  {return [vertxWrl2Canv $ix]}
  method heightWrl2Canv {iy} {
    set h [expr 1.0 * ($iy / $vy) * $ry] 
    return $h
  }

### Canv2Wrl coord space conversions

  method vertxCanv2Wrl {ix} {
    set x [expr 1.0 * ($ix / $rx) * $vx] ;# handle scaling
    return $x
  }

  method vertyCanv2Wrl {iy} {
    set iy [expr $iy - $ry]
    set y [expr 1.0 * ($iy / $ry) * $vy] ;# handle scaling
    return $y
  }

  method vertCanv2Wrl {vertex} {
    set ix [lindex $vertex 0]
    set iy [lindex $vertex 1]

    set result [list [vertxCanv2Wrl $ix] [vertyCanv2Wrl $iy]]
    return $result
  }

### Assertion/retraction

  method addNObj {name descriptors} {
    set taglist {}
    foreach el $descriptors {
      lappend taglist [eval $canvas create $el]
    }

    addNObjTags $name $taglist
  }

  method addNObjTags {name taglist} {
    set name2tag($name) $taglist

    foreach tag $taglist {
      $canvas addtag $name withtag $tag
    }

    setNObjPos $name {0 0} ;# starting position
    makeDraggable $name    ;# by default, make moveable
  }
    
  method delNObj {name} {
    if {![info exists name2tag($name)]} {
      puts "$this delNObj: $name not asserted in space, cannot delete"
      return
    }

    #Could delete items one by one, but since all should be tagged with
    # name, just do it all at once

    $canvas delete $name

    #set tags $name2tag($name)
    #foreach tag $tags {
    #  $canvas delete $tag
    #}

    #Clear entry from assoc array

    unset name2tag($name)
    if {[info exists name2pos($name)]} { ;#delete name2pos, if present
      unset name2pos($name)
    }
  }

  method setNObjPos {name pos} {
    ## Saves in world coords, not canv coords

    set name2pos($name) $pos
  }
    
  method getNObjPos {name} {
    ## Saves in world coords, not canv coords

    if {![info exists name2pos($name)]} {return {}} ;# doesn't exist
    return $name2pos($name)
  }

  method moveNObj {name pos} { 
    set lastpos [getNObjPos $name]
    if {$lastpos == {}} {

      puts "$this moveNObj: can't run, because no existing pos for $name"
      puts "exists; ignoring"
      return
    }

    set delta  [subCoords $pos $lastpos]
    setNObjPos $name $pos

    ## Actually do the move

    set ix [lindex $delta 0]
    set iy [lindex $delta 1]

    set dx [widthWrl2Canv $ix]
    set dy [heightWrl2Canv $iy]

    $canvas move $name $dx $dy
  }

  method addCoords {coorda coordb} { ;#slow, but could be substituted 

    set a1 [lindex $coorda 0]
    set a2 [lindex $coorda 1]
    
    set b1 [lindex $coordb 0]
    set b2 [lindex $coordb 1]

    set result [list [expr $a1 + $b1] [expr $a2 + $b2]]
    return $result
  }

  method subCoords {coorda coordb} { ;#slow, but could be substituted 

    set a1 [lindex $coorda 0]
    set a2 [lindex $coorda 1]
    
    set b1 [lindex $coordb 0]
    set b2 [lindex $coordb 1]

    set result [list [expr $a1 - $b1] [expr $a2 - $b2]]
    return $result
  }  

### Dragging methods

  method makeDraggable {name} {

    $canvas bind $name <ButtonPress-1> \
	   [format {%s selectDraggable %s %%x %%y} $this $name]

    $canvas bind $name <ButtonRelease-1> \
        [format {%s deselectDraggable %s} $this $name]
  }

  method selectDraggable {name ptrx ptry} {

    puts "select $name"
    
    set objpos [getNObjPos $name]

    set px   [vertxCanv2Wrl $ptrx]
    set py   [vertyCanv2Wrl $ptry]
    set ptroffset [subCoords [list $px $py] $objpos]
    
    bind $canvas <Motion>  [format {%s moveDraggable %s %%x %%y} $this $name]
    $canvas raise $name
  }

  method deselectDraggable {name} {
      bind $canvas <Motion> {}
  }

  method moveDraggable {name ptrx ptry} {

    set px   [vertxCanv2Wrl $ptrx]
    set py   [vertyCanv2Wrl $ptry]

    set newpos [subCoords [list $px $py] $ptroffset]
    moveNObj $name $newpos

  #  puts "move $name $newpos {$px $py} {$ptrx $ptry} {$ptroffset}"
    
    set lastptrx $ptrx
    set lastptry $ptry
  }

### Local members

  public local_members {canvprefix canvas rx ry vx vy}

  public canvas {.c}

  public name2tag 
  public name2pos

  #NOTE:  r[xy] and v[xy] must be assigned float values for method 
  # conversions to work
  
  public ycorrection {.9}
  public rx    {1280.} ;# real x ~ 1280
  public ry    {1024.} ;# real y ~ 1024
  public vx    {80.}
  public vy    {60.}

  public ptroffset {}
}

## END ##

