# Base client code for networked access
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/22/96
# Stripped from birdClient.tcl 11/20/96

package require Itcl
package require Tclx
package require tmg::base
package provide tmg::client 1.0

#################### Base Client class ####################

itcl_class baseClient {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]
 }

 method connect {} {
   if {$verbose} {puts "$this executing connect"}

   if {$host == {} || $port == {}} {
     puts "baseClient $this init: host/port info not provided! ($host/$port)"
     return
   }

   if {$TCL_X} {
     set serverhandle [server_connect $host $port]
   } elseif {$TCL_DP} {
     set serverhandle [lindex [dp_connect $host $port] 0]
   }

 }

 method disconnect {} {
   if {$verbose} {puts "$this calls disconnect"}
   set error [catch "close $serverhandle"]
   if {$error} {puts "$this disconnect closes with error $error"}
 }

 method startAutobuffer {} {
   fileevent $serverhandle readable "$this getBufferedStr"
   set autobuffer  1
   set autohandler 0
 }

 method stopAutobuffer {} {
   fileevent $serverhandle readable {}
   set autobuffer 0
 }

 method startAutohandler {} {
   fileevent $serverhandle readable "$this readableAutohandler"
   set autohandler 1
   set autobuffer  0
 }

 method stopAutohandler {} {
   fileevent $serverhandle readable {}
   set autohandler 0
 }

 method autobufferActive {} {return $autobuffer}

 method getServerHandle {} {return $serverhandle}
 method getBuffer {} {return $buffer}
 method getBufferLen {} {return [llength $buffer]}
 method clearBuffer {} {set buffer {}}

 method putStr {str {flush 1}} {
   if {$verbose} {puts "$this executing putStr \"$str\" $flush"}

   puts $serverhandle $str
   if {$flush} {catch "flush $serverhandle"}
 }

 method getStr {} {

   if {[eof $serverhandle]} {
     puts "<$this getStr:  server dies, completing disconnection>"
     disconnect
   }

   set str [string trim [gets $serverhandle]]
   return $str
 }

 method getBufferedStr {} {
   if {$verbose} {puts "$this executing getBufferedStr"}

   if {[eof $serverhandle]} {
     puts "<$this getStr:  server dies, completing disconnection>"
     catch disconnect
   }

   set str [string trim [gets $serverhandle]]
   lappend buffer $str
   return $str
 }

 method popBuffer {} { ;#pop a string off the top of the buffer, removing

   set str [lindex $buffer 0]
   set buffer [lrange $buffer 1 end]
   return $str
 }

 method readableAutohandler {} {
   set str [getStr]
   parse_msg $str
 }

 method parse_msg {msg} {
   puts "$this: dummy parse_msg handler received \"$msg\""
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

### Local Members ###

 public local_members {host port buffer autobuffer}

 public host {}
 public port {}

 public buffer {}
 public autobuffer  {0}
 public autohandler {0}

 # For the moment, retain for Wintel compatibility
 public TCL_DP {0}
 public TCL_X  {1}

 public serverhandle {}
}

## END ##

