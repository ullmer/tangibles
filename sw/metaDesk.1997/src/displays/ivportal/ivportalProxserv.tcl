# Inventor portal proxied-server code 
# Brygg Ullmer, MIT Media Lab TMG
# Begun 11/27/1996

# Because current generation of Wintel 3wish has Tcl-DP integrated, and
# (a) I don't want to rewrite a server class in Tcl-DP + (b) TclX doesn't
# yet seem to support servers on Wintel, + it's not integrated with the 
# Wintel 3wish, I've decided to write a proxied Inventor portal server
# on the PC.  This is a client that connects to an external server
# accepting server-requests on its behalf...

#package require Tclx
#We'll probably be running
package require tmg::client
package require tmg:metadesk::coordinator

package provide tmg::display:ivportal.proxserv 1.0

#################### IvPortal Proxied-Server ####################

itcl_class ivportalProxserv {

 inherit baseClient

 constructor {config} {
    set members [concat $members $local_members]
 }

 method init  {} {
    if {$verbose} {puts "$this calls init"}

    if {$capability == {}} {
      puts "$this init:  capability ID not specified"
      puts "Please supply specific proxserved ivportal capability to $this"
      puts "returning..."
      return
    }

    deskCoordinator $coordinator
    $coordinator init

    $coordinator registerCapability $capability proxserv
    set host [$coordinator getServerHost $capability]
    set port [$coordinator getServerPort $capability]

    ## Start net client
    connect
 }

 method enterIdleLoop {} {
   tiIdle "$this graphicsIdleCallback"
 }

 method graphicsIdleCallback {} {

   set results {}
   set updates [getUpdates]

   foreach update $updates {
     set command [expandCRString $update]
     set result  [eval $command]
     lappend results [collapseCRString $result]
   }

   putStr [format {PROXSERV RETURN RESULTS \{%s\}} $results]
 }

 method getUpdates {} {

   putStr {PROXSERV GET UPDATES}
   set updates [getStr]

   return $updates
 }

 public local_members {coordinator capability}

 public coordinator {proxportalcoord}

 #Multiple proxserved ivportals will likely be running in any given app.
 # Thus, leave capability undefined, and force instance to specify
 # particulars.  BAU 11/27/96

 #Original pass:
 #  public capability  {tmg::display:ivportal.proxserv}
 #Plausible samples:
 #  public capability  {tmg:metadesk::display:alens.proxserv}
 #  public capability  {tmg:metadesk::display:desk.proxserv}

 public capability  {}

}

