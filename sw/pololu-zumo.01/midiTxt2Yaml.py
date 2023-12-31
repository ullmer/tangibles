# Import text dump from exMidi03, and attempt to make it more legible + actionable
# Brygg Ullmer, Clemson University
# Begun 2023-12-27

#Example lines:

#output: Microsoft GS Wavetable Synth 0
#48 360 C3 0.20689649999999998
#60 2508 C4 0.20689649999999998
#60 2508 C4 0.20258615625
#60 2508 C4 0.00431034375
#60 2508 C4 0.20258615625
#53 2509 F3 0.00431034375
#57 2509 A3 0.20689649999999998
#65 2509 F4 0.20689649999999998
#65 2509 F4 0.20258615625

import librosa
import sys

sys.stdout.reconfigure(encoding='utf-8')

fn = '3400themerrypheastevenritchie.txt'
#fn='midi-tst01d.txt'

f  = open(fn, 'rt')
rawlines = f.readlines()

firstBegun = 0
lastBegun  = 0
sameTimeThresh = 1 #if time difference within N milliseconds, assume ~chord
#sameTimeThresh = 15 #if time difference within N milliseconds, assume ~chord
queuedNotes    = []

noteDict = {}

for rawline in rawlines:
  if rawline[0:3] == 'out': continue #ignore MIDI output debug messages
  cleanline = rawline.rstrip() # remove newline

  try:
    fields = cleanline.split(' ')
    nv, tb, wn, v, nd = fields
    noteVal, timeBegun, whichNote, whichVel, noteDuration = int(nv), int(tb), wn, int(v), float(nd)
    if lastBegun == 0: lastBegun = timeBegun ; firstBegun = timeBegun
    diffTime = timeBegun - lastBegun

    #outStr = "- {noteDelay: %4i, noteVals: %s}" % (diffTime, queuedNotes)
    if whichVel != 0: noteDict[noteVal] = timeBegun - firstBegun
    else:
      noteBegun    = noteDict[noteVal]
      currentTime  = timeBegun   - firstBegun
      noteDuration = currentTime - noteBegun
      n = librosa.midi_to_note(noteVal)

      outStr = "- [%4i, %3i, %i, %s]" % (noteBegun, noteVal, noteDuration, n)
      print(outStr)

    lastBegun = timeBegun; queuedNotes = [noteVal]

  except: print("oops:", len(fields), fields)

### end ###
