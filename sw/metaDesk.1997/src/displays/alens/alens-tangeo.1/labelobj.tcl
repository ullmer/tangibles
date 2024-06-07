# Simple graphical label object
# Brygg Ullmer, MIT Media Lab TMG
# Begun 10/25/96

source base.tcl

#################### Label Object ####################

itcl_class labelObject {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]
 }

 method assertIv {} {

   addNObj $this [format {
     DEF %s:translation Translation {translation %s}
     DEF %s:material    Material {}
     DEF %s:cube        Cube {width %s depth %s height %s}
     DEF %s:textmaterial Material {diffuseColor 1 1 1}  
     DEF %s:font        Font {name "Helvetica" size 15}
     DEF %s:textpush    Translation {translation 0 0 %s}
     DEF %s:text        Text2 {justification CENTER}
    } $this $location $this $this $width $depth $height $this $this \
      $this $depth $this]
 }

 method switchState {newstate} {
   ;# Switch to a specified state

   if {[string match $state $newstate]} {return} ;# already there

   foreach el $states {
     if {[string match $newstate [lindex $el 0]]} {
       set state $newstate
       set text  [lindex $el 1]
       set color [lindex $el 2]

       tweakNObj $this:material [format {diffuseColor %s} $color]
       tweakNObj $this:text     [format {string "%s"} $text]
       return
     }
   }
 }

 method toggle {} {
   ;# Toggle to the next state

   set numstates [llength $states]

   #Find which state in the list we occupy
   set whichstate 0; set i 0
   foreach el $states {
     if {[string match $state [lindex $el 0]]} {set whichstate $i}
     incr i
   }

   incr whichstate ;#send us to the next state

   if {$whichstate >= $numstates} {set whichstate 0}
   switchState [lindex [lindex $states $whichstate] 0]
 }

 public local_members {location state states width height depth}

 public location {0 0 0}
 public state {NULL}
 public states {{OFF Off {1 0 0}} {ON On {0 1 0}}}
 public width   8
 public height  8
 public depth   1
}

## END ##

