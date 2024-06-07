# Package command "proxy" for pre-7.5/4.1 Tcl (e.g., old 3wish) to handle
# package inlines
# Brygg Ullmer, MIT Media Lab TMG
# Begun 11/30/1996

## Check to see if we need this code

set tclversion [info tclversion]
if {$tclversion >= 7.5} { #We already have packages!

  puts "Package proxy lib: Tcl version $tclversion already in use"
  puts "package proxy command will not be loaded"
  return
}

## OK, we do

puts "Package proxy lib: Tcl version $tclversion is less than 7.5"
puts "package proxy command loading..."

global TMG_BASE_SRC ULLMER_BASE_SRC TMG_SENSORS TMG_DISPLAYS TMG_PACKAGE_LIST

# Unix version
set TMG_BASE_SRC    {/mas/tangible/src/tangeo.2/src}
set ULLMER_BASE_SRC {/mas/tangible/u/ullmer/pb/code}

# Wintel version

set TMG_SENSORS   "$TMG_BASE_SRC/sensors"
set TMG_DISPLAYS  "$TMG_BASE_SRC/displays"
set TMG_RESOURCES "$TMG_BASE_SRC/resources"

set TMG_PACKAGE_LIST " \
   \{tmg::base        $TMG_RESOURCES/base.tcl} \
   \{tmg::client      $TMG_RESOURCES/client.tcl} \
   \{tmg::server      $TMG_RESOURCES/server.tcl} \
   \{tmg::graphview   $TMG_SENSORS/vision/graphview.tcl} \
   \{tmg:metadesk::coordinator            $TMG_RESOURCES/coordinator.tcl} \
   \{tmg:metadesk::sensor:flock.calibrate \
      $TMG_SENSORS/flock/birdCalibrate.tcl} \
   \{tmg:metadesk::sensor:flock.client    $TMG_SENSORS/flock/flockClient.tcl} \
   \{tmg:metadesk::sensor:flock.server    $TMG_SENSORS/flock/flockServer.tcl} \
   \{tmg:metadesk::sensor:flock.flocklib  {}} \
   \{tmg:metadesk::sensor:lego.client     $TMG_SENSORS/lego/legoClient.tcl} \
   \{tmg:metadesk::sensor:lego.legolib    {}} \
   \{tmg:metadesk::sensor:lego.server     $TMG_SENSORS/lego/legoServer.tcl} \
   \{tmg:metadesk::sensor:tagtrack.client  \
      $TMG_SENSORS/vision/tagtrackClient.tcl}  \
   \{tmg:metadesk::sensor:tagtrack.server \
      $TMG_SENSORS/vision/tagtrackServer.tcl} \
   \{tmg:metadesk::sensor:vision.server    \
      $TMG_SENSORS/vision/visionClient.tcl} \
   \{tmg:metadesk::sensor:vision.visionlib \
      $TMG_SENSORS/vision/visionServer.tcl} \
" 
 
################### Package proxy-command ######################### 
 
proc package {command packagename} { 
} 

