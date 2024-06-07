# Bird wrapper code for networked access
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96

global __BIRDCLIENT__
if {[info exists  __BIRDCLIENT__]} {return}
set  __BIRDCLIENT__ 1

source base.tcl
source machtype
source ports

#################### Bird Wrapper ####################
# High bandwidth client

itcl_class flockHIBWClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portBIRDPULL
    set port $portBIRDPULL
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

 method getPosition {{device BIRD1}} {
   puts $serverhandle [format {%s GET POSITION} $device]
   flush $serverhandle
   set  pos [string trim [gets $serverhandle]]

   return $pos
 }

 method getOrient {{device BIRD1}} {
   puts $serverhandle [format {%s GET ORIENTATION} $device]
   flush $serverhandle
   set  orient [string trim [gets $serverhandle]]

   return $orient
 }

 public local_members {host port}

 public host gumby.media.mit.edu
 public port 8020

 public serverhandle {}
}

#################### Bird Wrapper ####################

# Low bandwidth client

itcl_class flockLOBWClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portBIRDPULL
    set port $portBIRDPULL
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

 method getPosition {{device BIRD1}} {
   
   switch $device {
     BIRD1 {set birdnum 0}
     BIRD2 {set birdnum 1}
     default {return {}}
   }

   set vals [lindex $netupdate $birdnum]
   set result [lrange $vals 0 2]

   return $result
 }

 method getOrient {{device BIRD1}} {

   switch $device {
     BIRD1 {set birdnum 0}
     BIRD2 {set birdnum 1}
     default {return {}}
   }

   set vals [lindex $netupdate $birdnum]
   set result [lrange $vals 3 5]

   return $result
 }

 method getNetUpdate {} {
   puts $serverhandle "SERVER GET ALL"
   flush $serverhandle

   set lastnetupdate $netupdate
   set netupdate [string trim [gets $serverhandle]]
 }

 public local_members {host port lastnetupdate netupdate}

 public host gumby.media.mit.edu
 public port 8020

 public lastnetupdate {}
 public netupdate {}
 public serverhandle {}
}

## END ##

