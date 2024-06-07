#!3wish

#Vision ReServer
#Brygg Ullmer, MIT Media Lab TMG
#Begun October 26, 1996

source visionRS2Lib.tcl
source ports

## Port for vision reserver
global portVISIONPULL
set port $portVISIONPULL

objectManager objmgr
visionPushClient visionclient -objectManager objmgr

visionclient init

######################## Quit Button #####################

button .q -text Quit -command shutdown; pack .q
proc shutdown {} {
    global server_handle
    
    puts "Shutting down"
    close $server_handle
    
    #no idea what this does
    w3Die #try this...
}

######################## Get Lego Query ################

proc getVisionQuery {obj query} {
    
    puts "Lego query:  $apos $aorient"
    
    puts "query is: $query"
    switch $query {
	"ANALOG" {
	    return [getLegoAnalogData $port]
	}
	default {
	    return {}
	}
    } 
    
}

######################## Parse Message ################

proc parse_msg { request } {

    #syntax: [VISOBJ] GET CONFIG
    
    if { [llength $request] == 3 } {
	set visobjword [lindex $request 0]
	set getword    [lindex $request 1]
	set queryword  [lindex $request 2]

	##Kinda ugly, but special case for server get objlist

	if {[string match $visobjword "SERVER"]} {
	  #ok, they're asking the server something

	  if {[string match $getword "GET"] &&
	      [string match $queryword "OBJLIST"]} {

	      return [objmgr getObjList]
	  }

	  if {[string match $getword "GET"] &&
	      [string match $queryword "ALLOBJS"]} {

	      return [objmgr getAllObjs]
	  }

	  puts "bad request of SERVER: $queryword (query)"
	  return {}
	}

	if {![string match "GET" $getword] } {
	    puts "bad request: $request (get)"
	    return
	}

	set r [objmgr getObjVal $visobjword]

	if {[string match "POSITION" $queryword]} {
	  set answer [lrange $r 0 1]
	} elseif {[string match "ORIENTATION" $queryword]} {
	  set answer [lindex $r 2]
	} else {set answer {}}


	if { [clength $answer] == 0 } {
	    puts "bad request: $request (query)"
	    return {}
	} else {
	    return $answer
	}
    } else {
	puts "bad request: $request (word count)"
    }

  return
}

############################ NET CODE STARTS #######################

########################### Add Client #############################

#when a client connects, add him to the list of clients
proc add_client {} {
    
    global server_handle clients
    
    puts "adding a client"
    set client [server_accept $server_handle]
    
    lappend clients $client
    fileevent $client readable "handle_client_request $client"

}

######################### Handle Client Request #########################

proc handle_client_request {client} {

   global clients

   if {[eof $client]} { ;# Client died; remove him from the list
     puts "eof $client"
     close $client

     set index [lsearch $clients $client]
     if {$index != -1} {
       set clients [lreplace $clients $index $index]
     }

     return
   }
        
   if { [llength [lindex [select $client {} {} 0] 0]] == 1 } {
      catch {set in_msg [gets $client]}
            
      #if we got a valid request from this client
      if { [info exists in_msg] && $in_msg != {}} {

        puts $client [parse_msg [string trim $in_msg]]
        flush $client
      }
   }
}

############################ NET CODE STARTS #######################

#bird server

set server_handle [server_create -myport $port]
set clients {}

puts "server started"

#### Set up server
#set hook to add a client

fileevent $server_handle readable add_client

## END ##

