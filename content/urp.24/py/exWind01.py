# Successive illustrative examples of local & distributed (second) Wind
# Brygg Ullmer, Clemson University
# Begun 2024-05-20

WIDTH, HEIGHT = 1920, 1080

w       = Actor('wind21e')
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

#### when touchpad/mouse pressed ####

def on_mouse_down(pos): 
  if w.collidepoint(pos): touched['current'] = 'wind'

#### when touchpad/mouse released ####
     
def on_mouse_up():        touched['current'] = None

### end ###
