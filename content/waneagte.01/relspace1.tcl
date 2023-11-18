#Freedom's first (proxied) program in Wish3
#12/1/95, proxy Brygg


###################### Read File ##########################

proc readfile {file} {
  set f [open $file r]
  set result ""

  while {![eof $f]} {
    append result [gets $f] "\n"
  }

  return $result
}    

###################### Read File ##########################

proc readlist {file} {
  set f [open $file r]
  set result {}

  while {![eof $f]} {
    lappend result [gets $f] 
  }

  return $result
}    

###################### Get El ##########################

proc get_el {name el} {

  upvar #0 GLcontrols controls
  set els $controls($name)

# puts "<$name/$el/$els>"

  switch $el {
    location {set i 1}
    sound    {set i 2}
    duration {set i 3}
    playradii {set i 4}
    killradii {set i 5}
  }

# puts "<$i>"
  return [lindex $els $i]
}

###################### Setup Controls ##########################

proc setup_controls {} {

  global control_data names
  set control_data [readlist "control.data"]

## This is sort of ugly/obtruse, but... get over it! :-)
  upvar #0 GLcontrols controls
  upvar #0 GLpid     pid
  upvar #0 GLplaying playing

  foreach el $control_data {
    set name [lindex $el 0]
    if {[string match $name ""]} {continue}
    set controls($name) $el
    set playing($name)  0
    lappend names $name
  }
}

################## Periodic Callback #####################

proc callback {} {
 
  global names
  upvar #0 GLpid     pid
  upvar #0 GLplaying playing

  set camposition [getCamPosition]
  set camposition [lreplace $camposition 1 1 0]

  foreach name $names { 

    set objlocation [get_el $name location]
    set objlocation [lreplace $objlocation 1 1 0]
    set distance    [dist3D $camposition $objlocation]

    if {$distance < [get_el $name playradii] && ![set playing($name)]} {

      puts "play $name $distance ([get_el $name sound])"
      set playing($name) 1
      exec playaiff [format {/video/common/freedom/%s} [get_el $name sound]] &

#      tiAfter [get_el $name duration] [format {
#           upvar #0 GLplaying playing
#	    set playing(%s) 0} $name]

    }
  }
}

####################


puts "Reading Model file..."
set fbvar [readfile "place17.iv"]
puts "Model read"

addNObj temple $fbvar

puts "assertions complete"

setup_controls

tiPeriodic 0.5 {callback}

