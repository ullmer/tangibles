# Simple Flock test program
# Brygg Ullmer, MIT Media Lab TMG
# Begun 11/30/1996

package require Tclx
package require tmg:metadesk::sensor:flock.client

flockLOBWClient fc
fc init

#addNObj birdGeom {Cube {}}

#tiIdle {...} ;# if in Inventor
while {1} {

  fc getNetUpdate
  set pos [fc getPosition BIRD1]
  set rot [fc getOrient   BIRD1]

  puts "Bird1: position <$pos>, orientation <$rot>"

#  rotNObj  birdGeom:rot $rot
#  moveNObj birdGeom:trans $pos

  sleep 1
}  

