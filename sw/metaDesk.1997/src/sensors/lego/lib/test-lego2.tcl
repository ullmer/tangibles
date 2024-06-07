package require tmg:metadesk::sensor:lego.legolib

#initLegoDacta /dev/ttyd2
initLegoDacta /dev/ttyd1

while {1} {

  puts "Lego [getLegoAnalogData 1]"
  exec sleep 1

}

