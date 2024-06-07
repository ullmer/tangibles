# Serves pushed Vision update in pull vision
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96

source base.tcl
source graphview.tcl
source machtype
source ports

#################### vision Push Wrapper ####################

itcl_class visionPushClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portVISIONPUSH
    set port $portVISIONPUSH
 }

 method init  {} {
   global TCL_DP TCL_X

## Establish connection

   if {$TCL_DP} {
     set serverhandle [lindex [dp_connect $host $port] 0]
     dp_send $serverhandle "GET"
   } elseif {$TCL_X} {
     set serverhandle [server_connect -buf $host $port]
     server_send $serverhandle "GET"
   }

   puts "visionPush client connected to $host $port"

## Setup handler for pushed events
   if {$TCL_DP} {
      eval [format {
	tiIdle {
	  if {[lindex [dp_isready %s] 0]} { 
	    %s process_request }
	  }
       } $serverhandle $this]
   } elseif {$TCL_X} {
      fileevent $serverhandle readable "$this process_request"
   }
 }

 method close {} {
   global TCL_DP TCL_X

   close $serverhandle
 }

 method process_request {} {
   global TCL_DP TCL_X

   if {$TCL_DP} {
      #set inline [dp_receive $serverhandle]
      set inline [gets $serverhandle] 
   } elseif {$TCL_X} {
      set inline [gets $serverhandle] 
   }

   puts "$inline"

   set command [string trim $inline]

   if {[info exists objectManager]} {
     $objectManager process_vision_update $command
   }
 }

 public local_members {host port objectManager}

 public host gumby.media.mit.edu
 public port 8010
 public objectManager

 public serverhandle {}
}

#################### Object Manager ####################

itcl_class objectManager {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    set vismon visionMon
    visionMonitor $vismon
    $vismon init
 }

 method process_vision_update {bigupdate} {

   $vismon displayVistags $bigupdate

   foreach update $bigupdate { #takes multi-message update
     set obj [lindex $update 0]
     set command [lindex $update 1]
     set x   [lindex $update 2]
     set y   [lindex $update 3]
     set rot [lindex $update 4]

     regsub {^(object:)(.*)$} $obj {\2} obj

     if {[lsearch $objlist $obj] == -1} {lappend objlist $obj}
     set objassoc($obj) [format {%s %s %s} $x $y $rot]
   }
 }

 method getObjVal {obj} {
   if {[info exists objassoc($obj)]} {
     return $objassoc($obj)
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

 method getObjList {} {return $objlist}

 public local_members {objlist}

 public vismon {}

 public objlist {}
 public objassoc 
}

## END ##

