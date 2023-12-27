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

fn = '3400themerrypheastevenritchie.txt'
f  = open(fn, 'rt')
rawlines = f.readlines()

lastBegun  = 0
lastOutStr = ''

for rawline in rawlines:
  if rawline[0:3] == 'out': continue #ignore MIDI output debug messages
  cleanline = rawline.rstrip() # remove newline

  try:
    f = cleanline.split(' ')
    noteVal, timeBegun, whichNote, noteDuration = int(f[0]), int(f[1]), f[2], float(f[3])
    outStr = "%s %i" % (whichNote, timeBegun-lastBegun)
    if outStr != lastOutStr: print(outStr); lastOutStr = outStr
    lastBegun = timeBegun
  except: print("oops:", len(fields), fields)

### end ###
