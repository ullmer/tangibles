#Flock of Birds server
#Brygg Ullmer, MIT Media Lab TMG
#Begun 11/23/1996

package require tmg::server
package require tmg:metadesk::coordinator
package require tmg:metadesk::sensor:flock.flocklib
package require tmg:metadesk::sensor:flock.calibrate

package provide tmg:metadesk::sensor:flock.server 1.0

###################### Vision Server #####################

itcl_class flockServer {

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

    puts "$this initiating flock..."
    initFlock "/dev/ttyd2"
    puts "Flock initiated."

    flockDeskCalibration $calibrate

    ## Start net server
    startServer
  }

  method parse_msg {msg client} {
    if {$verbose} {puts "$this calls parse_msg $msg"}

    if {[regexp {GET POSITION} $msg]} { ;# get position
      set whichbird [lindex $msg 0]
      regsub {BIRD([0-9])} $whichbird {\1} id
      incr id -1   ;# Chris was using sensor 1/2

      set pos [getFlockPos $id]
      set apos [$calibrate mapAPos $pos]

      if {$verbose} {puts "$this parse_msg returns bird $id position $apos"}

      putStr $client $apos
      return
    }

    if {[regexp {GET ORIENTATION} $msg]} { ;# get orientation
      set whichbird [lindex $msg 0]
      regsub {BIRD([0-9])} $whichbird {\1} id
      incr id -1   ;# Chris was using sensor 1/2

      set orient [getFlockOrient $id]
      set aorient [$calibrate mapAOrient $orient]

      if {$verbose} {puts "$this parse_msg returns bird $id orient $aorient"}

      putStr $client $aorient
      return
    }

    if {[string match {SERVER GET ALL} $msg]} { ;# get all

      if {$verbose} {puts "$this parse_msg enters get all"}

      set all [getFlockAll]

      set b1 [lindex $all 0]
      set b2 [lindex $all 1]

      set ab1 [format {%s %s} \
	[$calibrate mapAPos    [lrange $b1 0 2]] \
	[$calibrate mapAOrient [lrange $b1 3 5]]]

      set ab2 [format {%s %s} \
	[$calibrate mapAPos    [lrange $b2 0 2]] \
	[$calibrate mapAOrient [lrange $b2 3 5]]]

      set result [list $ab1 $ab2]

      if {$verbose} {puts "$this parse_msg returns bird all $result"}

      putStr $client $result
      return
    }
  }

  public local_members {
    coordinator capability 
  }

  public coordinator {flockcoord}
  public capability  {tmg:metadesk::sensor:flock}

  public calibrate {flockcalib} 

}

##END##

