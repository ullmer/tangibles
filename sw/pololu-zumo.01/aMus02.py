# Demo of music playing with callbacks for LED and display effects.

from zumo_2040_robot import robot
from musicSupport import *

song = "V3 T200 cf...a>c... <f >a#dfdc"

zumoPrep()

buzzer.play_in_background(song)
#motors.set_speeds(1000, 1000)
motors.set_speeds(1500, 1500)

zumoLoop(song)

### end ###

