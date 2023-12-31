import sys, time
import mido, librosa

#https://github.com/mido/mido
#https://librosa.org/doc/main/generated/librosa.midi_to_note.html

#example used with permission: https://www.classicalmidi.co.uk/music3/3400themerrypheastevenritchie.mid
mfn = 'music/3400themerrypheastevenritchie.mid'

#mfn = 'merryChristmas.mid'
#mfn='midi-tst01b.mid'

mid = mido.MidiFile(mfn)

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

def currentTime(): return round(time.time() * 1000)
#def bendTime():    return time.time() * 2.
#def bendTime():    return time.time() / 6.
  
n = librosa.midi_to_note(60) #experiencing 1-2s latency on first 
                             #librosa call, so this needs to happen
                             #before mid-playback use

firstTime = currentTime()

port = mido.open_output(outport)
sys.stdout.reconfigure(encoding='utf-8') #sharps and flats :-)

#https://mido.readthedocs.io/en/latest/api.html#mido.MidiFile.play
#for msg in mid.play(now=bendTime):

for msg in mid.play():
  #print(msg)
  diffTime = currentTime() - firstTime
  try:    n = librosa.midi_to_note(int(msg.note))
  except: continue

  try:    print(msg.note, diffTime, n, msg.velocity, msg.time)
  except: print("err:", msg)

  port.send(msg)

### end ###
