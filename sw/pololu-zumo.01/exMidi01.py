import mido

#https://github.com/mido/mido
#https://librosa.org/doc/main/generated/librosa.midi_to_note.html

#mfn = 'merryChristmas.mid'
#mfn = '3400themerrypheastevenritchie.mid'
mfn='midi-tst01b.mid'
mid = mido.MidiFile(mfn)

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

port = mido.open_output(outport)

for msg in mid.play():
  port.send(msg)
  print(msg)

### end ###
