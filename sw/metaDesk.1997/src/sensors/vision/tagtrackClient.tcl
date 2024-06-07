#Tagtrack client
#Brygg Ullmer, MIT Media Lab TMG
#Begun 11/22/1996

package require tmg::client
package require tmg:metadesk::coordinator 
package provide tmg:metadesk::sensor:tagtrack.client 1.0


###################### Tagtrack Client #####################

itcl_class tagtrackClient {

  inherit baseClient

  constructor {config} {
    set members [concat $members $local_members]
  }

  method init {} {

    deskCoordinator $coordinator 
    $coordinator init

    $coordinator registerCapability $capability client
    set host [$coordinator getServerHost $capability]
    set port [$coordinator getServerPort $capability]

    connect
    startAutohandler
    putStr {SUBSCRIBE TAGTRACK}
  }

  method parse_msg {msg} {

    if {$verbose} {puts "$this calls parse_msg $msg"}

    set lastframe    $currentframe
    set currentframe $msg

    if {$externalCallback != {}} {eval $externalCallback [list $msg]}
  }

  method getFrame     {} {return $currentframe}
  method getLastFrame {} {return $lastframe}

#### Local Members ####

  public local_members {coordinator lastframe currentframe externalCallback}

  public coordinator {ttcoord}
  public capability  {tmg:metadesk::sensor:tagtrack}

  public lastframe    {}
  public currentframe {}

  public externalCallback {}

}

## END ##

