# Import text dump from exMidi03, and attempt to make it more legible + actionable
# Brygg Ullmer, Clemson University
# Begun 2023-12-27


import time, mido

mo  = mido.open_output()

notes=[60,53,57]

while True:
  for n in notes: mo.send(mido.Message('note_on', note=n))
  time.sleep(.6)

### end ###
