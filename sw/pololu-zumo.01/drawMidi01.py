# Example of drawing MIDI events
# Brygg Ullmer, Clemson University
# Begun 2023-12-27

midiValsPerOctave = 12
pixelsPerVal      = 4
midiValsTotal     = 127
midiValOctaves    = int(midiValsTotal / midiValsPerOctave)

scaleGray = (10, 10, 10)
scaleRed  = (100, 0,  0)

HEIGHT = midiValsTotal * pixelsPerVal
WIDTH  = 1200

######################## draw grid ########################

def drawGrid(currentX):
  x1, x2 = 0, WIDTH
  y      = pixelsPerVal
  x3     = currentX

  for octIdx in midiValOctaves:
    draw.line((x1,y1), (x2,y2), scaleGray)

  draw.line((x3, 0), (x3, HEIGHT), scaleRed)

######################## draw ########################

def draw():
  drawGrid(100)

### end ###
