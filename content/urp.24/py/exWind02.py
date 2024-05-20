# Successive illustrative examples of local & distributed (second) Wind
# Brygg Ullmer, Clemson University
# Begun 2024-05-20

WIDTH, HEIGHT = 1920, 1080
import moveWinHome #move window to 0,0 / top-left of screen

w       = Actor('wind21e3')
b1      = Actor('wind21j-bldg3', pos=(850, 450))
b2      = Actor('wind21s-bldg3', pos=(350, 650))
actors  = [w, b1, b2]
touched = {'current': None}

#### draw ####

def draw(): 
  screen.clear()
  for a in actors: a.draw()

#### handle simplest interactivity ####

def on_mouse_up():        touched['current'] = None

def on_mouse_down(pos): 
  for a in actors:
    if a.collidepoint(pos): touched['current'] = a

def on_mouse_move(rel):
  dx, dy = rel

  for a in actors:
    if touched['current'] == a:
      x1, y1 = a.pos
      x2, y2 = x1+dx, y1+dy
      a.pos  = (x2, y2)

### end ###
