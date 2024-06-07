#Vision server
#Brygg Ullmer, MIT Media Lab TMG
#Begun November 4, 1996
#Rebuilt around tangeo::server November 4, 1996

package require tmg::server
package require tmg:metadesk::coordinator
package require tmg:metadesk::sensor:tagtrack.client
package require tmg:metadesk::sensor:vision.visionlib
package require tmg::graphview
package require tmg:metadesk::sensor:lego.client

package provide tmg:metadesk::sensor:vision.server 1.0

###################### Vision Server #####################

itcl_class visionServer {

  inherit baseServer

  constructor {config} {
    set members [concat $members $local_members]
  }

  method init {} {
    if {$verbose} {puts "$this calls init"}

    deskCoordinator $coordinator
    $coordinator init

    $coordinator registerCapability $capability server
    set port [$coordinator getServerPort $capability]

    ## Connect to tagtrack server
    set tagtrack ttclient
    tagtrackClient $tagtrack -externalCallback "$this proc_newframe" \
       -verbose 0
    $tagtrack init

    ## setup fields assoc array
    set i 0
    foreach el $fields {
      set fieldid($el) $i
      incr i
    }

    ## Start up objman

    CVobjectManager $objman -verbose 0

    ## Call graphview monitor

    visionMonitor $vismon
    $vismon init

    ## Start net server
    startServer
  }

  method proc_newframe {incoming_frame} {

    if {$verbose} {puts "$this calls proc_newframe $incoming_frame"}

    set ttframe [clip_bottom $incoming_frame]

    set scene      [$objman generateScene]
    set visionMask [$objman generateVisionMask $scene]

    set labeler_result [labelScene $visionMask $ttframe $scene]

    #set labeler_result [labelScene last $ttframe $scene]

    set newscene [lindex $labeler_result 0]

    if {$verbose} {puts "$this proc_newframe synths scene \{$newscene\}"}
    puts "labelScene -> $newscene"

    set lastframe    $currentframe
    set currentframe $newscene

    $objman process_vision_update $currentframe

#    set entranceEvent [$objman genEntranceEvent]
#    set eec [$objman getEECtr]
#    if {$entranceEvent != {}} {
#      puts "entrance event $eec \{$entranceEvent\}"
#    }

    $vismon displayScenetags $newscene
  }

  method parse_msg {msg client} {
    if {$verbose} {puts "$this calls parse_msg $msg"}

    if {[string match $msg {SERVER GET ALLOBJS}]} {
      if {$verbose} {puts "$this parse_msg gets allobjs"}

	set response [$objman getAllObjs]

     set entranceEvent [$objman genEntranceEvent]
     if {$entranceEvent != {}} {
        puts "entrance event \{$entranceEvent\}"
	set ee [list {ENTRANCE} $entranceEvent]
	lappend response $ee        
     }


      
      puts "sending client <$response>"
      putStr $client $response
    }
  }

  method restruct_visclient {scenelist} {
    set result {}

    if {$verbose} {puts "$this calls restruct_visclient \{$scenelist\}"}

    foreach el $scenelist {
      set name [lindex $el 0]
      set pos  [lindex $el 1]
      set rot  [lindex $el 2]

      set r [format {%s %s %s} $name $pos $rot]
      lappend result $r
    }

    if {$verbose} {puts "$this restruct_visclient returns \{$result\}"}
    return $result
  }

#### Vision blob-processing utils #####

  method clip_bottom {framelist} { ;# clip off lamps and bottom-dwellers

    set result {}
    foreach entry $framelist {
      set y [get_field $entry rely] ;#  this perhaps is cleaner
     if  {$y < [lindex $mincenter 1]} {continue} ;# clip out
      lappend result $entry
    }

    return $result
  }

  method get_field {targetline name} {

    set fieldnum $fieldid($name)
    if {$fieldnum == {}} {return {}} ;# bogus field
    return [lindex $targetline $fieldnum]
  }

#### Local Members ####

  public local_members {
    coordinator capability tagtrack tagtrack_frame currentframe lastframe
    minccenter maxcenter maxx
  }

  public coordinator {viscoord}
  public capability  {tmg:metadesk::sensor:vision}

  public tagtrack {}
  public tagtrack_frame {}

  public currentframe {}
  public lastframe {}

  public mincenter {.17 .1} ;#clips lamps, and leaves right 110-pixel margin
  public maxcenter {1. 1.}
  public maxx {.9} ;# for rectified image

  public fieldid
  public fields {blobnum relx rely mass ecc angle majorx majory majore minore}

  public objman {CVobjman}
  public vismon {gvismon}
#  public scene  {medialab dome}

}

#################### Object Manager ####################

itcl_class CVobjectManager {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

 #   set vismon visionMon
 #   visionMonitor $vismon
 #   $vismon init

     legoLOBWClient $lc
     $lc init
     $lc getNetUpdate
 }

 method process_vision_update {newframe} {

  # $vismon displayVistags $newframe

   foreach update $newframe { #takes multi-message update
     set obj [lindex $update 0]
     set pos [lindex $update 1]
     set rot [lindex $update 2]
     set certainty [lindex $update 3]
     set timealive [lindex $update 4]

     if {[lsearch $objlist $obj] == -1} {
	lappend objlist $obj
	set objpresent($obj) 0
     }

     set objassoc($obj) [format {%s %s %s %s} $pos $rot $certainty $timealive]
     set objtimestamp($obj) $masterTimestamp
     set objtryingtoenter($obj) 1
   }

   incr masterTimestamp
   if { [expr fmod($masterTimestamp,$legoUpdateFreq)] == 0 } {

       $lc getNetUpdate
   }
 }

 method generateVisionMask {scene} { ;# I'm not completely sure of this...

   set result {}

   foreach obj $objlist {
       if {[checkObjPresent $obj] && [lsearch $scene $obj] != -1} {
	 set oa  $objassoc($obj)
	 set pos [lrange $oa 0 1]
	 set rot [lindex $oa 2]
	 set certainty [lindex $oa 3]
	 set timealive [lindex $oa 4]

       lappend result [list $obj $pos $rot $certainty $timealive]
     }
   }
   return $result
 }

 method checkObjDeparture {obj} {
   if {![info exists objtimestamp($obj)] ||
       ![info exists objtryingtoenter($obj)] ||
       ![info exists objpresent($obj)]} {
     return 0
   }

   set age [expr $masterTimestamp - $objtimestamp($obj)]
   if {$objpresent($obj) && $age > $departureAge} {
     set objpresent($obj) 0
     set objtryingtoenter($obj) 0
     
     return 1
   }

   return 0
 }

 method checkObjEntrance {obj} {
   if {![info exists objtimestamp($obj)] || 
       ![info exists objtryingtoenter($obj)] ||
       ![info exists objpresent($obj)]} {
     return 0
   }

   if {$objtryingtoenter($obj) && !($objpresent($obj))} {
     set objpresent($obj) 1
     return 1
   }

   return 0
 }

 method checkObjPresent {obj} {

   if {![info exists objpresent($obj)]} {return 0}
   return $objpresent($obj)
 }

 method getObjVal {obj} {
   if {[info exists objassoc($obj)]} {
     return $objassoc($obj)
   }

   return {}
 }

 method genEntranceEvent {} {

   # will return an entrance event, if one's to be had

   if {$verbose} {puts "$this calls genEntranceEvent"}

   foreach obj $objlist {
     if {[checkObjDeparture $obj]} {
       if {$verbose} {puts "$this: $obj departure"}

       set result [format {%s leave} $obj]
       incr entranceEventCtr
       return $result
     }

     if {[checkObjEntrance $obj]} {
       if {$verbose} {puts "$this: $obj entrance"}

       set result [format {%s enter} $obj]
       incr entranceEventCtr
       return $result
     }
   }

   return {}
 }

 method getAllObjs {} {
  
   set result {}
   set objs [getObjList]

   foreach el $objs {
     set val [getObjVal $el]
     if {$val != {}} {
       lappend result [format {%s %s} $el $val]
     }
   }

   return $result
 }

 method generateScene {} {
     # s is what lego expects to be on desk
     # scene is what was expected on desk last time
     set s {}
     if { [$lc getAnalogData 1] > 1000 } {
	 lappend s dome
     }
     if { [$lc getAnalogData 2] > 1000 } {
	 lappend s media
     }
     if { [$lc getAnalogData 3] > 1000 && [$lc getAnalogData 4] > 1000} {
	 set s {media dome}
     }

     set si3 [intersect3 $scene $s]

     set sLeave [lindex $si3 0]
     set sEnter [lindex $si3 2]

     if { [llength $sLeave] == 0 && [llength $sEnter] == 0 } {
	      puts "scene is: $scene"
	 return $scene
     }

     set s [lindex $si3 1]
     set s [concat $sEnter $s]

     set scene $s
     puts "scene is: $scene"

     return $scene
 }

 method getObjList {} {return $objlist}

 method getEECtr {} {return $entranceEventCtr}

 public local_members {objlist}

 public vismon {}

 public objlist {}
 public objtimestamp
 public objassoc 
 public objpresent
 public objtryingtoenter
 public masterTimestamp {0}
 public departureAge {10} ;# if he hasn't been seen in N timeincs...
 public scene {medialab dome}
 public entranceEventCtr {0}
 public lc {}
 public legoUpdateFreq 3
}


## END ##



