# Flock wrapper code for networked access
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96
# Integrated as package, 11/23/1996 

package require tmg::client
package require tmg:metadesk::coordinator

package provide tmg:metadesk::sensor:flock.client 1.0

#################### Flock high-bandwidth client ####################

itcl_class flockHIBWClient {

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

 method getPosition {{device BIRD1}} {
   putStr  [format {%s GET POSITION} $device]
   set pos [getStr]

   return $pos
 }

 method getOrient {{device BIRD1}} {
   putStr    [format {%s GET ORIENTATION} $device]
   set orient [getStr]

   return $orient
 }

 public local_members {coordinator capability}

 public coordinator {flockcoord}
 public capability  {tmg:metadesk::sensor:flock}
}

#################### Flock low bandwidth client ####################

itcl_class flockLOBWClient {

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

 method getPosition {{device BIRD1}} {
   
   switch $device {
     BIRD1 {set birdnum 0}
     BIRD2 {set birdnum 1}
     default {return {}}
   }

   set vals   [lindex $netupdate $birdnum]
   set result [lrange $vals 0 2]

   return $result
 }

 method getOrient {{device BIRD1}} {

   switch $device {
     BIRD1 {set birdnum 0}
     BIRD2 {set birdnum 1}
     default {return {}}
   }

   set vals   [lindex $netupdate $birdnum]
   set result [lrange $vals 3 5]

   return $result
 }

 method getNetUpdate {} {
   putStr {SERVER GET ALL}

   set lastnetupdate $netupdate
   set netupdate     [getStr]
 }

 public local_members {coordinator capability}

 public coordinator {flockcoord}
 public capability  {tmg:metadesk::sensor:flock}
 
 public lastnetupdate {}
 public netupdate {}
}

## END ##

