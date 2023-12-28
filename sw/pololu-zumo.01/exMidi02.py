import sys, time
import mido, librosa

#https://github.com/mido/mido
#https://librosa.org/doc/main/generated/librosa.midi_to_note.html

#mfn = 'merryChristmas.mid'
#mfn = '3400themerrypheastevenritchie.mid'
mfn = 'midi-tst01b.mid'
mid = mido.MidiFile(mfn)

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

def currentTime(): return round(time.time() * 1000)

n = librosa.midi_to_note(70)

firstTime = currentTime()

port = mido.open_output(outport)
sys.stdout.reconfigure(encoding='utf-8')

for msg in mid.play():
  port.send(msg)
  #print(msg)
  diffTime = currentTime() - firstTime
  n = librosa.midi_to_note(int(msg.note))
  print(msg.note, diffTime, n, msg.time)

### end ###
