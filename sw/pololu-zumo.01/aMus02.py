# Demo of music playing with callbacks for LED and display effects.

from zumo_2040_robot import robot
from musicSupport import *
import enoTurtle

song  = "V3 T200 cf...a>c... <f >a#dfdc"
dance = "f50 r50" * 4         # a square dance :-)

zumoPrep()

buzzer.play_in_background(song)
enoTurtle.followPattern(dance)

zumoLoop(song)

### end ###

