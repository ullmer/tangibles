# Lego client code 
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96
# Integrated as package, 11/26/1996 

package require Tclx
package require tmg::client
package require tmg:metadesk::coordinator

package provide tmg:metadesk::sensor:lego.client 1.0

#################### Lego Client ####################
# High bandwidth client

itcl_class legoHIBWClient {

 inherit baseClient

 constructor {config} {
    set members [concat $members $local_members]
 }

 method init  {} {
    if {$verbose} {puts "$this calls init"}

    deskCoordinator $coordinator
    $coordinator init

    $coordinator registerCapability $capability client
    set host [$coordinator getServerHost $capability]
    set port [$coordinator getServerPort $capability]

    ## Start net client
    connect
 }

 method getAnalogData {port} {

   putStr "LEGO GET ANALOG $port"
   set val [getStr]

   return $val
 }

 public local_members {coordinator capability}

 public coordinator {legocoord}
 public capability  {tmg:metadesk::sensor:lego}
}

#################### Lego client ####################
# Low bandwidth client

itcl_class legoLOBWClient {

 inherit baseClient

 constructor {config} {
    set members [concat $members $local_members]
 }

 method init  {} {
    if {$verbose} {puts "$this calls init"}

    deskCoordinator $coordinator
    $coordinator init

    $coordinator registerCapability $capability client
    set host [$coordinator getServerHost $capability]
    set port [$coordinator getServerPort $capability]

    ## Start net client
    connect
 }

 method getAnalogData {port} {

   set i [expr $port - 1]

   set val [lindex $netupdate $i]

   return $val
 }

 method getNetUpdate {} {
     putStr {LEGO GET ANALOG ALL}
     
     set lastnetupdate $netupdate
     #set netupdate [getStr]
     set netupdate [lindex [getStr] 0]
 }

 public local_members {coordinator capability lastnetupdate netupdate}

 public lastnetupdate {}
 public netupdate {}

 public coordinator {legocoord}
 public capability  {tmg:metadesk::sensor:lego}
}

## END ##

