# Import text dump from exMidi03, and attempt to make it more legible + actionable
# Brygg Ullmer, Clemson University
# Begun 2023-12-27

#Example lines:

#- [2148, [48]]
#- [ 134, [60, 53, 57, 65, 58, 70]]
#- [ 204, [70, 65]]
#- [ 205, [62]]
#- [ 204, [65]]

import yaml, mido, time

yfn = '3400themerrypheastevenritchie3.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

mo  = mido.open_output()

for row in yd:
  delayVal, notes = row
  for note in notes: mo.send(mido.Message('note_on', note=note))
  time.sleep(delayVal/1000.)
  
### end ###


