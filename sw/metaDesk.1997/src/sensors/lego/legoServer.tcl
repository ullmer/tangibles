#Lego server
#Brygg Ullmer, MIT Media Lab TMG
#Begun 11/26/1996

#Modified: by lopes 1/8/96
#############
#this server now automatically polls the lego box every $touchTime milliseconds
#and tries to get the same values from it 3 times in a row
#when a client makes a request, he is always sent the cached value
#to insure that he is given valid data
#this may result in the data given to the client being up to $touchTime ms old
#an alternative approach might be to actually honor the client's request
#instead of using the cache
#note: the server assumes only lego ports 1-4 are used at this time
#to insure more validity of data

package require tmg::server
package require tmg:metadesk::coordinator
package require tmg:metadesk::sensor:lego.legolib

package provide tmg:metadesk::sensor:lego.server 1.0

###################### Lego Server #####################

itcl_class legoServer {

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

    puts "$this initiating lego..."
    initLegoDacta "/dev/ttyd1"
    puts "Lego initiated."

      #setup cache
      $this initCache


    ## Start net server
    startServer
    idleToucher
  }

  method initCache {} {
      set i 0
      while { $i < $cacheSize } {
	  lappend cache {0 0 0 0 0 0 0 0}
	  incr i
      }
      puts "cache size is [llength $cache]"
      getData
      puts "$this: cache initiated"
  }


  method getData {} {
      $this add_value [lindex [getLegoAnalogData ALL] 0]
      while {![$this cache_valid]} {
	  $this add_value [lindex [getLegoAnalogData ALL] 0]
      }
  }
  
  method getCachedVal {} {
      return [lindex $cache [expr $cacheSize - 1]]
  }

  method idleToucher {} {
    $this getData
    after $touchTime  "$this idleToucher" 
      ;# touch self every 1 seconds to keep legos alive.  
      ;# Known lego hardware feature/bug
  }

  method touch {} {
    getLegoAnalogData 0 ;# read from lego pad 0
    #if {$verbose} {puts "$this touch"}
  }

#  method parse_msg {msg client} {
#    if {$verbose} {puts "$this calls parse_msg $msg"}
#
#    if {[regexp {LEGO GET ANALOG} $msg]} { ;# get position
#      set id [lindex $msg 3]
#      if {$verbose} {puts "$this parse_msg $msg $client: port $id"}
#      set val [getLegoAnalogData $id]
#
#      if {$verbose} {puts "$this parse_msg returns port $id val $val"}
#
#      putStr $client $val
#      return
#    }
#  }

  method parse_msg {msg client} {
      if {$verbose} {puts "$this calls parse_msg $msg"}
      
      if {[regexp {LEGO GET ANALOG} $msg]} { ;# get position
      set id [lindex $msg 3]
	  if {$verbose} {puts "$this parse_msg $msg $client: port $id"}

	  set tval [$this getCachedVal]

	  if { "$id" == "ALL" } {
	      set val [list $tval]
	  } else {
	      if { $id > 0 && $id < 9 } {
		  set val [lindex $tval [expr $id - 1]]
	      } else {
		  set val -1
	      }
	  }
			   
	  if {$verbose} {puts "$this parse_msg returns port $id val $val"}
	  
	  putStr $client $val
	  return
      }
  }
  

  method cache_valid {} {

      set l1 {}
      set l2 {}
      set l3 {}
      set l4 {}

      foreach el $cache {

	  lappend l1 [lindex $el 0]
	  lappend l2 [lindex $el 1]
	  lappend l3 [lindex $el 2]
	  lappend l4 [lindex $el 3]

      }

      if { [withinTolerance $l1] && [withinTolerance $l2] && 
	   [withinTolerance $l3] && [withinTolerance $l4] } {
	  return 1
      }
      return 0

  }

  method withinTolerance {valList} {
      
      #find max and min val in list, and sum
      set sum 0
      set maxVal [lindex $valList 0]
      set minVal $maxVal
      foreach el $valList {
	  set sum [expr $sum + $el ]
	  if { $el > $maxVal } {
	      set maxVal $el
	  }
	  if { $el < $minVal } {
	      set minVal $el
	  }
      }
      set avgVal [expr $sum / [llength $valList]]
      if { $avgVal == 0 } {
	  set sway 0
      } else {
	  set sway [expr (( $maxVal - $minVal ) / $avgVal) * 100 ]
      }

      if { $sway > $cacheTolerance } {
	  return 0
      }
      return 1


  }
      
  method add_value {val} {

      #this assumes we only care about lego ports 1-4
      foreach el [lrange $val 4 7] {
	  if { $el < 1000 } {

	      return
	  }
      }

      set i 1
      while { $i < $cacheSize } {
	  set im1 [expr $i - 1]
	  set cache [lreplace $cache $im1 $im1 [lindex $cache $i]]
	  incr i
      }

      set csm1 [expr $cacheSize - 1]
      set cache [lreplace $cache $csm1 $csm1 $val]

  }

  public local_members {
    coordinator capability 
  }

  public coordinator {legocoord}
  public capability  {tmg:metadesk::sensor:lego}

  public calibrate {legocalib} 
  public cache {}
  public touchTime {1000}
  public cacheSize 3
  public cacheTolerance 10
}

##END##




