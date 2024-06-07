# Lego wrapper code for networked access
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96

global __LEGOCLIENT__
if {[info exists  __LEGOCLIENT__]} {return}
set  __LEGOCLIENT__ 1

source base.tcl
source machtype
source ports

#################### Lego Wrapper ####################
# High bandwidth client

itcl_class legoHIBWClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portLEGOPULL
    set port $portLEGOPULL
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

 method getAnalogData {port} {

   puts $serverhandle "LEGO GET ANALOG $port"
   set val [string trim [gets $serverhandle]]

   return $val
 }

 public local_members {host port}

 public host speedy.media.mit.edu
 public port 8030

 public serverhandle {}
}

#################### Bird Wrapper ####################

# Low bandwidth client

itcl_class legoLOBWClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]

    global portLEGOPULL
    set port $portLEGOPULL
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

 method getAnalogData {port} {

   set i [expr $port - 1]

   set val [lindex $netupdate $i]

   return $val
 }

 method getNetUpdate {} {
   puts $serverhandle "LEGO GET ANALOG ALL"
   flush $serverhandle

   set lastnetupdate $netupdate
   set netupdate [string trim [gets $serverhandle]]
 }

 public local_members {host port lastnetupdate netupdate}

 public host speedy.media.mit.edu
 public port 8030

 public lastnetupdate {}
 public netupdate {}
 public serverhandle {}
}

## END ##

