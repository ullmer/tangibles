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

import time, mido

mo  = mido.open_output()

fn = '3400themerrypheastevenritchie.txt4'
f  = open(fn, 'rt')
rawlines = f.readlines()

lastBegun  = 0
lastOutStr = ''

for rawline in rawlines:
  if rawline[0:3] == 'out': continue #ignore MIDI output debug messages
  cleanline = rawline.rstrip() # remove newline

  try:
    fields = cleanline.split(' ')
    nv, tb, wn, nd = fields
    noteVal, timeBegun, whichNote, noteDuration = int(nv), int(tb), wn, float(nd)
    if lastBegun == 0: lastBegun = timeBegun
    diffTime     = timeBegun - lastBegun; lastBegun=timeBegun

    mo.send(mido.Message('note_on', note=noteVal))
    if diffTime > 0: time.sleep(diffTime/1000.)
    print(fields)

  except: print("oops:", len(fields), fields)

### end ###
