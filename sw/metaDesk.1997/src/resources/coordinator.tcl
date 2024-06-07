# Base code for capability coordinator
# Brygg Ullmer, MIT Media Lab TMG
# Begun 11/22/1996

package require Itcl
package require Tclx
package require tmg::base
package require tmg::server 

package provide tmg:metadesk::coordinator 1.0

#################### Base Server class ####################

;# Currently implement with a lookup table

itcl_class deskCoordinator {

 inherit base

 constructor {config} {
   set members [concat $members $local_members]
 }

 method init {} { ;# establish connection

   ;# hardwire this for the moment
   foreach capability $hardwire_capabilities {
     set name   [lindex $capability 0]
     set server [lindex $capability 1]
     set port   [lindex $capability 2]

     set hostTable($name) $server
     set portTable($name) $port
   }
 }

 method registerCapability {capability cliser} {
  # call with capability name and spec of client/server.  
  # Returns handle to instance id
 }

 method getServerHost {capability} {
   set host {}

   if {[info exists hostTable($capability)]} {
     set host $hostTable($capability)
   }

   return $host
 }

 method getServerPort {capability} {
   set port {}

   if {[info exists portTable($capability)]} {
     set port $portTable($capability)
   }

   return $port
 }

 method registerServerRequest {capability callback} {
   # call with capability whose server is desired
   # Also provide callback for re-invoking capability when available
 }

 method registerServerDeath {capability {callback {}}} {
   # call with capability whose server has failed
   # optionally provide callback for re-invoking capability when available
 }

######### Local member data ###########

 public local_members {capabilities}

 public capabilities {}

 public hostTable
 public portTable

 public serverRegistry
 public clientRegistry

 public availabilityCallbacks

 public hardwire_caplabels {name host port}
 public hardwire_capabilities {
   {tmg:metadesk::sensor:tagtrack gumby 8000}
   {tmg:metadesk::sensor:vision   gumby 8001}
   {tmg:metadesk::sensor:flock    gumby 8002}
   {tmg:metadesk::sensor:lego     gumby 8003}
   {tmg:metadesk::display:desk    pinky 8010}
   {tmg:metadesk::display:plens   pinky 8011}
   {tmg:metadesk::display:alens   grasp 8020}
 }
}

## END ##


