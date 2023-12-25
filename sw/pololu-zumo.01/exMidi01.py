import mido

mfn = 'merryChristmas.mid'
mid = mido.MidiFile(mfn)

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

port = mido.open_output(outport)

for msg in mid.play():
  port.send(msg)

### end ###
