# Example of drawing MIDI events
# Brygg Ullmer, Clemson University
# Begun 2023-12-27

midiValsPerOctave = 12
pixelsPerVal      = 5
midiValsTotal     = 127
midiValOctaves    = int(midiValsTotal / midiValsPerOctave)

scaleGray = (50, 50, 50)
scaleRed  = (100, 0,  0)

HEIGHT = midiValsTotal * pixelsPerVal
WIDTH  = 1200

######################## draw grid ########################

def drawGrid(currentX):
  x1, x2 = 0, WIDTH
  y      = pixelsPerVal
  x3     = currentX

  for octIdx in range(midiValOctaves):
    screen.draw.line((x1,y), (x2,y), scaleGray)
    y += midiValsPerOctave * pixelsPerVal

  screen.draw.line((x3, 0), (x3, HEIGHT), scaleRed)

######################## draw ########################

def draw():
  screen.fill((10, 10, 20))
  drawGrid(100)

### end ###
