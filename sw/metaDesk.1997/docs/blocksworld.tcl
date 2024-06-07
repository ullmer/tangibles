Listing of /mas/tangible/u/ullmer/pb/code/blockworld.1/blockworld.tcl

Files sensorDevices.tcl, displayDevices.tcl, and base.tcl are 
(net)sourced, at present from the same directory.  Min and Chris are
familiar with displayDevices, formerly deskDevices; it in turn depends on
birdClient, legoClient, visionClient, which in turn call birdServer, 
legoServer, and visionServer, presently symlinked via synth.1

Good stuff!  BAU

-------------------------------

# First test of simple proxdist blocks world
# Brygg Ullmer, MIT Media Lab TMG
# Begun 11/08/96

package require tmg:metadesk::displays
package require tmg:metadesk::sensors
package require tmg:metadesk::base

############################ Blocks World ###########################

itcl_class blocksWorld {

  inherit base

  constructor {config} {
    set members [concat $members $local_members]
  }


#### Main manipulation functions

  method addBlock {name position} {

    if {$verbose} {puts "$this addBlock called on $name // $position"}

    if {[getBlockPresent $name] == 1} {
      puts "$this addBlock error: Block $name already present; ignoring..."
      return
    }

    ## Add the block
    lappend blocklist $name
    setBlockCoord $name $position

    set lensObject {
      DEF $name:pos  Translation {translation $position}
      DEF $name:lift Translation {translation 0 0 2.5}
      DEF $name:obj  Cube        {width 5 height 5 depth 5}
    }

    set lensObject [expandVars $lensObject]

    enterScope tmg:metadesk

    deskDisplay  evalCommand "addNObj $name $deskObject"
    alensDisplay evalCommand "addNObj $name $deskObject"
  }

  method deleteBlock {name} {

    if {$verbose} {puts "$this deleteBlock called on $name"}

    set index [lindex $blocklist $name]

    if {$index == -1} {
      puts "$this delBlock error: obj $name doesn't exist, ignoring"
      return
    }

    ## Delete it from the list
    set objlist [lreplace $objlist $index $index]

    enterScope tmg:metadesk

    deskDisplay  evalCommand "delNObj $name" 
    alensDisplay evalCommand "delNObj $name"
  }

  method moveBlock {name position} {

    if {$verbose} {puts "$this moveBlock called on $name // $position"} 

    lappend position 0 ;# Add Z coordinate

    enterScope tmg:metadesk

    deskDisplay  evalCommand "moveNObj $name:pos $position"
    alensDisplay evalCommand "moveNObj $name:pos $position"
  }

  method updateBlocks {} {

    if {$verbose} {puts "$this updateBlocks called"} 

    enterScope tmg:metadesk

    set visobjs   [visionObjTracker getObjs]
    set viscoords [visionObjTracker getObjCoords]

    ## Delete objects which have departed

    foreach block $blocklist {
      if {[lsearch $visobjs $block] == -1} {
	deleteBlock $block
      }
    }

    ## Update old blocks/add new blocks 
    
    foreach el $viscoords {

      set block [lindex $el 0]
      set pos   [lindex $el 1]

      if {[getBlockPresent $block]} { ;# it's present, update it
	moveBlock $block $pos
      } else { ;# it's new, add it
	addBlock $block $pos
      }
    }
  }

### Convenience functions

  method getBlockPresent {name} {
    if {[lsearch $blocklist $name] == -1} {return 0}
    return 1
  }

  method setBlockCoord {name coord} {set blockcoords($name) $coord}
  method getBlockCoord {name} {return $blockcoords($name)}
  method getBlockList  {}     {return $blocklist}

  method getBlockCoords {} {
    set result {}

    foreach block $blocklist {
      set coord [getBlockCoord $block]
      lappend result [list $block $coord]
    }

    return $result
  }

### Class variables

  public local_members {blocklist verbose}

  public blocklist {}
  public verbose {1}
  public blockcoords 
}

## END ##

