#!3wish

#Tagtrack wrapper 
#Brygg Ullmer, MIT Media Lab TMG
#Begun November 4, 1996

source ports

## Port for vision reserver
global portTAGTRACKPUSH
set port $portTAGTRACKPUSH

###################### Tagtrack Wrapper #####################

itcl_class tagtrackWrapper {

  method init {} {
    ## Set up update callback 
    fileevent stdin readable "$this update"
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

      puts -nonewline "[llength $visionFrame] "; flush stdout

    } else {
      lappend queue $inline
    }
  }

  public visioncycleCallback {broadcastTTUpdate [getLastFrame]}
  public visionFrame {}
  public queue {} 
}

###################### broadcast Tagtrack Update ###################

proc broadcastTTUpdate {update} {
  global clients

  foreach client $clients {
    if {![eof $client]} { ;# as long as he's alive, sent him the update

      puts $client $update
      flush $client
    }
  }
}

######################## Quit Button #####################

button .q -text Quit -command shutdown; pack .q
proc shutdown {} {
    global server_handle
    
    puts "Shutting down"
    close $server_handle
    
    #no idea what this does
    w3Die #try this...
}

######################## Parse Message ################

proc parse_msg { request } {
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

        #puts $client [parse_msg [string trim $in_msg]]
        puts $client "No request handler in place"
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

tagtrackWrapper ttwrapper

ttwrapper init ;# this starts it all off

## END ##

