#Inventor portal server code
#Brygg Ullmer, MIT Media Lab TMG
#Begun 11/27/1996

package require tmg::server
package require tmg:metadesk::coordinator

package provide tmg::display:ivportal.server 1.0

###################### Lego Server #####################

itcl_class ivportalServer {

  inherit baseServer

  constructor {config} {
    set members [concat $members $local_members]
  }

  method init {} {
    if {$verbose} {puts "$this calls init"}

    if {$capability == {}} {
      puts "$this init:  capability ID not specified"
      puts "Please supply specific proxserved ivportal capability to $this"
      puts "returning..."
      return
    }

    deskCoordinator $coordinator
    $coordinator init

    $coordinator registerCapability $capability server
    set port [$coordinator getServerPort $capability]

    ## Start net server
    startServer
  }

  method parse_msg {msg client} {
    if {$verbose} {puts "$this calls parse_msg $msg"}

    if {[regexp {LEGO GET ANALOG} $msg]} { ;# get position
      set id [lindex $msg 3]
      if {$verbose} {puts "$this parse_msg $msg $client: port $id"}
      set val [getLegoAnalogData $id]

      if {$verbose} {puts "$this parse_msg returns port $id val $val"}

      putStr $client $val
      return
    }
  }

  method bindToDisplayDimension {displayDimension} {}

### Local Members ###

  public local_members {
    coordinator capability 
  }

  public coordinator {legocoord}

  #Plausible samples:
  #  public capability  {tmg:metadesk::display:alens.server}
  #  public capability  {tmg:metadesk::display:desk.server}

  public capability  {}

}

##END##

