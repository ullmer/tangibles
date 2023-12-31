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

#example used with permission: https://www.classicalmidi.co.uk/music3/3400themerrypheastevenritchie.mid
yfn = 'music/3400themerrypheastevenritchie.yaml'
#yfn='midi-tst01d.yaml'

yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

mo  = mido.open_output()

lastTime = 0
for row in yd:
  timeVal, note, duration, noteStr = row
  if lastTime == 0: lastTime = timeVal
  delayVal = timeVal-lastTime

  if delayVal > 0: time.sleep(delayVal/1000.)
  mo.send(mido.Message('note_on', note=note))

  #time.sleep(duration/1000.)
  #mo.send(mido.Message('note_on', note=note, velocity=0))
  #lastTime = timeVal + duration
  lastTime = timeVal
  
### end ###


