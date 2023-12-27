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

######################## place window @ 0,0 ####################

#magic for placing at 0,0
import platform, pygame
if platform.system() == "Windows":
  from ctypes import windll
  hwnd = pygame.display.get_wm_info()['window']
  windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)

######################## cursor ########################

class cursor:
  cursorPos = 0
  def draw(self): screen.draw.line((self.cursorPos, 0), (self.cursorPos, HEIGHT), scaleRed)

######################## draw grid ########################

def drawGrid():
  x1, x2 = 0, WIDTH
  y      = pixelsPerVal

  for octIdx in range(midiValOctaves):
    screen.draw.line((x1,y), (x2,y), scaleGray)
    y += midiValsPerOctave * pixelsPerVal


######################## main ########################

c = cursor()
animate(c, cursorPos=WIDTH, duration=5.)

######################## draw ########################

def draw():
  screen.fill((10, 10, 20))
  drawGrid()
  c.draw()

### end ###
