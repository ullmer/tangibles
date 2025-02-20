# Example engaging class projects
# Brygg Ullmer, Clemson University
# Begun 2025-02-20

import sys, os, traceback

from enoMidiController import *
from projMidi          import *

################### main ################### 

emc = enoMidiController('aka_apcmini2', midiCtrlOutputId=4, activateOutput=True)  #A
pm  = ProjMidi(emc=emc)                                                      #B

emc.registerControls(pm.midiCB)   #C

#for i in range(64): emc.midiOut.note_on(i, i, 3)  # D (next 7 lines)
#for i in range(6): emc.midiOut.note_on(i, i, 3)
#blue 45 orange 5 green 25 brown 9

#for i in [45, 5, 25, 9]:  emc.midiOut.note_on(i, i,   1)
#for i in [46, 6, 26, 10]: emc.midiOut.note_on(i, i-1, 6)
#for i in [47, 7, 27, 11]: emc.midiOut.note_on(i, i-2, 10)

#for i in range(9):
#  for j in range(4):
#     cpgzam.setAkaiColorIdxCoord(j, j+4, i, 1)
  
def draw(): screen.clear(); pm.draw(screen)   #E
def update():               pm.update()
def on_mouse_down(pos):     pass #cpgzm.on_mouse_down(pos)

### end ###
