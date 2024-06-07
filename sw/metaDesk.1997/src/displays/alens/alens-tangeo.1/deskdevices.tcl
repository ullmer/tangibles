## Bird wrappers for Desk passiveLENS, activeLENS, and digitalLIGHT objects
## Brygg Ullmer, MIT Media Lab TMG
## Begun 10/25/96

global __DESKBIRDDEVICE__
if {[info exists  __DESKBIRDDEVICE__]} {return}
set  __DESKBIRDDEVICE__ 1

source base.tcl
source ports

#flockClient flock
#flock init

############################## plensTracker #########################

itcl_class plensTracker {

  inherit base

  constructor {config} {
     set members [concat $members $local_members]
  }

  method getPosition {} {
    set position [$birdResource getPosition $birdID]
    set orient   [$birdResource getOrient   $birdID]

    set x [lindex $position 0]
    set y [lindex $position 1]

    set heading [expr [lindex $orient 2] - 90]
    set dx [expr $trackerDisp * cos($heading*3.14159/180)]
    set dy [expr $trackerDisp * sin($heading*3.14159/180)]

    #set result "[expr $x + $dx] [expr $y + $dy] ($heading)"

    set result "[expr $x + $dx] [expr $y + $dy]"
    return $result
  }

  method getOrientation {} {
    set orient   [$birdResource getOrient   $birdID]
    set heading [expr [lindex $orient 2] - 90]

    return $orient
  }

  public local_members {birdResource birdID trackerDisp}

  public birdResource {}
  public birdID {BIRD2}
  public trackerDisp {10} ;#displacement defaults to 10 cm's
}

############################## alensTracker #########################

itcl_class alensTracker {

  inherit base

  constructor {config} {
     set members [concat $members $local_members]
  }

  method getPosition {} {
    set position [$birdResource getPosition $birdID]

    set x [lindex $position 0]
    set y [lindex $position 1]
    set z [lindex $position 2]

    set result [format {%s %s %s} \
      [expr $x - $xoffset] [expr $y - $yoffset] [expr $z - $zoffset]]

    return $result
  }

  method getOrientation {} {
    set orient   [$birdResource getOrient   $birdID]

    return $orient
  }

  public local_members {birdResource birdID xoffset yoffset zoffset}

  public birdResource {}
  public birdID {BIRD1}
  public xoffset {-8.9}
  public yoffset {12.1}
  public zoffset {-6.35}
}

############################# dlightTracker #########################

itcl_class dlightTracker {

  inherit base

  constructor {config} {
     set members [concat $members $local_members]
  }

  method getPosition {} {
    set position [$birdResource getPosition $birdID]

    set x [lindex $position 0]
    set y [lindex $position 1]
    set z [lindex $position 2]

    set result [format {%s %s %s} \  
      [expr $x - $xoffset] [expr $y - $yoffset] [expr $z - $zoffset]]

    return $result
  }

  method getOrientation {} {
    set orient   [$birdResource getOrient   $birdID]

    return $orient
  }

  public local_members {birdResource birdID xoffset yoffset zoffset}

  public birdResource {}
  public birdID {BIRD2}
  public xoffset {0}
  public yoffset {0}
  public zoffset {0}
}

############################# objtrayTracker #########################

itcl_class objtrayTracker {

  inherit base

  constructor {config} {
     set members [concat $members $local_members]
  }

  method objectPresent {objname} { 
    # returns 1 if present, 0 otherwise

    set port [getPort $objname]
    set data [$legoResource getAnalogData $port]

    if {$data < 300} {return 1} else {return 0} 
      #rough but reasonable threshold
  }

  method getObjectsPresent {{objseeklist {dome medialab}}} {

    # return list of objects that are present

    set result {}

    foreach el $objseeklist {
      if {[objectPresent $el]} {lappend result $el} 
    }
    ;# later use an mget for this

    return $result
  }

  method getObjectsNotPresent {{objseeklist {dome medialab}}} {

    # return list of objects that are present

    set result {}

    foreach el $objseeklist {
      if {![objectPresent $el]} {lappend result $el} 
    }
    ;# later use an mget for this

    return $result
  }


  method getPort {objname} {
    foreach el $portmaps {
      if {[string match $objname [lindex $el 0]]} {
	 return [lindex $el 1] ;# the lego port number
      } 
    }
  }

  public local_members {legoResource }

  public legoResource {}

  # The following are mappings from Dacta ports to phicon/instrument locations
  public portmaps {{dome 1} {medialab 2} {constinstr 3} 
     {dlight 4} {plens 5}}

}

############################# instrtrayTracker #########################

############################# visionObjTracker #########################

itcl_class visionObjTracker {
  ;# helps manage net-traffic and distributed state a bit 
  ;# time is getting short and need to keep things simple

  inherit base

  constructor {config} {
     set members [concat $members $local_members]
  }

  method getNetUpdate {} {
    set lastnetupdate $netupdate
    set netupdate [$visionResource getAllObjs]

    puts "getNetUpdate $netupdate"
  }

  method getPosition {obj} {
    #has intrinsic interpolation support

    set last {}
    set current {}

    foreach el $lastnetupdate {
      if {[string match $obj [lindex $el 0]]} {
	set last $el
      }
    }

    foreach el $netupdate {
      if {[string match $obj [lindex $el 0]]} {
	set current $el
      }
    }

    if {$current == {}} {return {}}
    if {$last == {}} {return [lrange $current 1 2]}

    #Normal case -- interpolate
    set val [interpolate [lrange $last 1 2] [lrange $current 1 2] $interpval]
    return $val

  }

  method getOrientation {obj} {
    #has intrinsic interpolation support

    set last {}
    set current {}

    foreach el $lastnetupdate {
      if {[string match $obj [lindex $el 0]]} {
	set last $el
      }
    }

    foreach el $netupdate {
      if {[string match $obj [lindex $el 0]]} {
	set current $el
      }
    }

    if {$current == {}} {return {}}
    if {$last == {}} {return [lindex $current 3]}

    #Normal case -- interpolate
    set val [interpolate [lindex $last 3] [lindex $current 3] $interpval]
    return $val

  }

  method interpolate {point1 point2 fraction} {

    if {[llength $point1] != [llength $point2]} {
      puts "bogus interpolation call, lengths don't match!"; return {}
    }

    set l [llength $point1]
    set result {}

    for {set i 0} {$i < $l} {incr i} {
      set di [expr ([lindex $point2 $i] - [lindex $point1 $i]) * $fraction]
      set el [expr [lindex $point1 $i] + $di]
      lappend result $el
    }

    return $result
  }

  public local_members {visionResource netupdate}

  public interpval {1} ;# default to fully the latest value
  public visionResource {}
  public netupdate {}
  public lastnetupdate {}
}
## END ##

