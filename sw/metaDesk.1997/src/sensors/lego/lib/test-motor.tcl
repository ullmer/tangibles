initLegoDacta /dev/ttyd2

while {1} {

  puts [getLegoAnalogData 2]

  if {[getLegoAnalogData 2] < 200} {setLegoMotorOn a 1
  } else { setLegoMotorOff a}

  sleep 1
}
