import sys, time
import mido, librosa

#https://github.com/mido/mido
#https://librosa.org/doc/main/generated/librosa.midi_to_note.html

#mfn = 'merryChristmas.mid'
mfn = '3400themerrypheastevenritchie.mid'
mid = mido.MidiFile(mfn)

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

def currentTime(): return round(time.time() * 1000)
#def bendTime():    return time.time() * 2.
#def bendTime():    return time.time() / 6.

firstTime = currentTime()

port = mido.open_output(outport)
sys.stdout.reconfigure(encoding='utf-8') #sharps and flats :-)


#https://mido.readthedocs.io/en/latest/api.html#mido.MidiFile.play

#for msg in mid.play(now=bendTime):

for msg in mid.play():
  #print(msg)
  port.send(msg)
  diffTime = currentTime() - firstTime
  try:    n = librosa.midi_to_note(int(msg.note))
  except: continue

  if msg.time != 0: 
    print(msg.note, diffTime, n, msg.time)
  else:
    print(msg.note, diffTime, n)

### end ###
