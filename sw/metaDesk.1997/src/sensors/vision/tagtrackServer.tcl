#Tagtrack server
#Brygg Ullmer, MIT Media Lab TMG
#Begun November 4, 1996
#Rebuilt around tangeo::server November 4, 1996

package require tmg::server
package require tmg:metadesk::coordinator

package provide tmg:metadesk::sensor:tagtrack.server 1.0

###################### Tagtrack Server #####################

itcl_class tagtrackServer {

  inherit baseServer

  constructor {config} {
    set members [concat $members $local_members]
  }

  method init {} {

    deskCoordinator $coordinator
    $coordinator init

    $coordinator registerCapability $capability server
    set port [$coordinator getServerPort $capability]

    ## Set up update callback 
    fileevent stdin readable "$this update"

    ## Start net server
    startServer
  }

  method getLastFrame {} {return $visionFrame} 

  method update {} {
    set inline [string trim [gets stdin]]
    set num [lindex $inline 0]

    if {$num == 0} {
      set visionFrame $queue
      set queue {}
      lappend queue $inline

      if {$visioncycleCallback != {}} {eval $visioncycleCallback}

      if {$verbose} {puts -nonewline "[llength $visionFrame] "; flush stdout}

    } else {
      lappend queue $inline
    }
  }

  method parse_msg {msg client} {
    if {$verbose} {puts "$this calls parse_msg $msg"}

    if {[string match $msg {SUBSCRIBE TAGTRACK}]} {
      if {$verbose} {puts "$this subscribes to tagtrack"}
      lappend subscribingClients $client
    }
  }

  method drop_client {client} {
    if {$verbose} {puts "$this calls drop_client $client"}

    baseServer::drop_client $client
    dropSubscriber $client
  }

  method dropSubscriber {client} {

    if {$verbose} {puts "$this calls dropSubscriber $client"}

    set index [lsearch $subscribingClients $client]
    if {$index == -1} {
      if {$verbose} {puts "$this dropSubscriber: $client not in subscribers"}
      return
    }

    # delete client from list
    set subscribingClients [lreplace $subscribingClients $index $index]
  }

######### Local Capabilities ########

  public local_members {
    coordinator capability visioncycleCallback visionFrame queue
  }

  public coordinator {ttcoord}
  public capability  {tmg:metadesk::sensor:tagtrack}

  public subscribingClients {}
  public visioncycleCallback {
     selectiveBroadcastStr $subscribingClients [getLastFrame]
  }
  public visionFrame {}
  public queue {} 
}

## END ##

