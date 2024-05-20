# Successive illustrative examples of local & distributed (second) Wind
# Brygg Ullmer, Clemson University
# Begun 2024-05-20

WIDTH, HEIGHT = 1920, 1080
import moveWinHome #move window to 0,0 / top-left of screen

w       = Actor('wind21e3')
touched = {'current': None}

#### draw ####

def draw(): screen.clear(); w.draw()

#### on mouse movement ####

def on_mouse_move(rel):
  dx, dy = rel

  if touched['current'] == 'wind':
    x1, y1 = w.pos
    x2, y2 = x1+dx, y1+dy
    w.pos  = (x2, y2)

#### handle simplest mouse interactivity ####

def on_mouse_up():        touched['current'] = None

def on_mouse_down(pos): 
  if w.collidepoint(pos): touched['current'] = 'wind'

### end ###
