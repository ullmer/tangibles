# Base server code for networked access
# Brygg Ullmer, MIT Media Lab TMG
# Begun 09/15/1996
# Reengineered 10/22/1996
# Stripped from birdServer.tcl 11/20/96

package require Itcl
package require Tclx
package require tmg::base
package provide tmg::server 1.0

#################### Base Server class ####################

itcl_class baseServer {

 inherit base

 constructor {config} {
   set members [concat $members $local_members]
 }

 destructor {stopServer}

 method startServer {} {
   if {$verbose} {puts "$this executing startServer"}

   set clients {}

   if {$port == {}} {
     puts "baseServer $this init: port not provided! ($port)"
     return
   }

   set serverhandle [server_create -myport $port]

   puts "Server $this started on port $port"

   #Add hook to add a client

   fileevent $serverhandle readable "$this add_client"
 }

 method stopServer {} {
   if {$verbose} {puts "$this executing stopServer"}

   #First, to avoid zombies, iterate through clients closing each connection 

   foreach client $clients {
     close $client
   }

   # Then, close serverhandle
   close $serverhandle
 }

 method add_client {} {
    if {$verbose} {puts "$this executing add_client"}
    
    puts "Server $this adding a client"
    set client [server_accept $serverhandle]
    
    fileevent $client readable "$this handle_client_request $client"
    lappend clients $client
 }

 method drop_client {client} {
   if {$verbose} {puts "$this executing drop_client $client"}

   puts "<$this: $client is dropped>"
   catch "close $client"

   set index [lsearch $clients $client]
   if {$index != -1} {
     set clients [lreplace $clients $index $index]
   }
 }


 method handle_client_request {client} {
   if {$verbose} {puts "$this executing handle_client_request $client"}

   ## Handle dead connection
   
   if {[eof $client]} { 
     puts "<$this: $client eofs>"
     drop_client $client
     return
   }

   # Get client request
   set error [catch "gets $client" in_msg]

   # Handle bogus response
   if {$error || ![info exists in_msg]} { 
     puts "<$this: $client dies ($error)>"
     drop_client $client
     return
   }

   set in_msg [string trim $in_msg]
   parse_msg $in_msg $client
   return
 }

 method parse_msg {msg client} {
   puts "$this: dummy parse_msg handler receives \"$msg\""
 }

 method broadcastStr {str {flush 1}} {
   selectiveBroadcastStr $clients $str $flush
 }

 method putStr {client str {flush 1}} {
   if {$verbose} {puts "$this executing putStr $client \"$str\" $flush"}

   puts $client $str
   if {$flush} {catch "flush $client"}
 }

 method selectiveBroadcastStr {targetclients str {flush 1}} {

   if {$targetclients == {}} {
     if {$verbose} {
       puts "$this executes selectiveBroadcastStr, has no targetclients"
     }
     return
   }

   if {$verbose} {puts "$this executing broadcastStr $str $flush"}

   foreach client $targetclients {

     if {[lsearch $clients $client] == -1} {
       if {$verbose} {puts "$this selectiveBroadcastStr: $client not connected"}
       continue
     }

     set error [catch "puts $client \{$str\}"]

     if {$error} {
       puts "$this broadcastStr:  error writing to $client!  Closing client..."
       drop_client $client
     }

     if {$flush} {catch "flush $client"}
   }
 }

 method collapseCRString {str} {
   set cstr [split $str "\n"]
   return $cstr
 }

 method expandCRString {strlist} {
   set result ""

   foreach el $strlist {
     append result $el "\n"
   }

   regsub "\n$" $result {} result ;#remove trailing CR
   return $result
 }

######### Local member data ###########

 public local_members {port clients buffer autobuffer}

 public port {}
 public clients {}

 public buffer {}
 public autobuffer {0}

 public serverhandle {}
}

## END ##


