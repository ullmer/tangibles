# Vision wrapper code for networked access
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96

source base.tcl
source machtype
source ports

#################### vision Pull Client ####################

itcl_class visionPullClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portVISIONPULL
    set port $portVISIONPULL
 }

 method init  {} {
   global TCL_DP TCL_X

   if {$TCL_DP} {
     set serverhandle [lindex [dp_connect $host $port] 0]
   } elseif {$TCL_X} {
     set serverhandle [server_connect $host $port]
   }
 }

 method close {} {
   global TCL_DP TCL_X

   close $serverhandle
 }

 method getPosition {objectname} {
   puts $serverhandle [format {%s GET POSITION} $objectname]
   flush $serverhandle
   set  pos [string trim [gets $serverhandle]]

   return $pos
 }

 method getOrient {objectname} {
   puts $serverhandle [format {%s GET ORIENTATION} $objectname]
   flush $serverhandle
   set  orient [string trim [gets $serverhandle]]

   return $orient
 }

 method getAllObjs {} {
   puts $serverhandle "SERVER GET ALLOBJS"
   flush $serverhandle
   return [string trim [gets $serverhandle]]
 }

 public local_members {host port}

 #public host gumby.media.mit.edu
 public host speedy.media.mit.edu
 public port 8011

 public serverhandle {}
}


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

   puts "visionPull client connected to $server $port"

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
   if {$TCL_DP} {
      #set inline [dp_receive $handle]
      set inline [gets $handle] 
   } elseif {$TCL_X} {
      set inline [gets $handle] 
   }

   #puts "$inline"

   set command [string trim $inline]

   puts "Eval'ing \"$command\""
   eval $command
 }

 public local_members {host port}

 public host gumby.media.mit.edu
 public port 8010

 public serverhandle {}
}

#################### tagtrack Client ####################

itcl_class tagtrackClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portTAGTRACKPUSH
    set port $portTAGTRACKPUSH
 }

 method init  {} {
   global TCL_DP TCL_X

   if {$TCL_DP} {
     set serverhandle [lindex [dp_connect $host $port] 0]
   } elseif {$TCL_X} {
     set serverhandle [server_connect $host $port]
   }


## Setup handler for pushed events
   if {$TCL_DP} {
      eval [format {
	tiIdle {
	  if {[lindex [dp_isready %s] 0]} { 
	    %s recordUpdate }
	  }
       } $serverhandle $this]
   } elseif {$TCL_X} {
      fileevent $serverhandle readable "$this recordUpdate"
   }
 }

 method close {} {
   global TCL_DP TCL_X

   close $serverhandle
 }

 method getFrame {} {return $current_inline}

 method recordUpdate {} {

   set current_inline [gets $serverhandle]
   return $current_inline
 }

 method adjustCoord {tagtrackcoord}  {

    set x [lindex $tagtrackcoord 0]
    set y [lindex $tagtrackcoord 1]

    #trap is the ratio of vision trapezoid bottom to top
    set trap 1.2244898

    #puts "old x was: $x"

    set x [expr 1. - $x]

    set q [expr ( 1. - $y ) + $y * ( 1. / $trap ) ]
    set x [expr ( 1. - $q ) / 2. + $q * $x ]

    set mx [expr (54.5 * $x) + 4.3]
    set my [expr (43.3 * $y) + 5.5]

    set result [list $mx $my]

    return $result
 }


 method getLocationList {} {
   set frame [getFrame]
   set result {}

   foreach blob $frame {
     set position [lrange $blob 1 2]
     set mposition [adjustCoord $position]
     lappend result $mposition
   }

   return $result
 }


 public local_members {host port}

 #public host gumby.media.mit.edu
 public host gumby.media.mit.edu
 public port 8011

 public current_inline {}

 public lastframe {}
 public currentframe {}

 public serverhandle {}
}


