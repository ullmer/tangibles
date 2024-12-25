import os

WIDTH, HEIGHT=480, 1920
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

def drawRects():
  numRects = 12; h = 70; dy = 150
  color    = 35, 25, 25
  for i in range(numRects):
    y0  = i*dy + 80
    box = Rect((0, y0), (WIDTH, h))
    screen.draw.filled_rect(box, color)

def draw():
  screen.clear()
  drawRects()

### end ###
