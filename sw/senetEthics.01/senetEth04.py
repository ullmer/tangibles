# Senet ethics example
# Brygg Ullmer, Clemson University
# Begun 2026-03-24

WIDTH, HEIGHT=1535,1180

a  = Actor('senet03k')

peopleAbbrev = ['gel', 'jgh', 'tr', 'fdr', 'er', 'rf']
people = []; x, y = 300, 500; dx = 100
for pa in peopleAbbrev: 
  p = Actor(pa); people.append(p)
  p.pos = (x,y); x+= dx

def draw(): 
  a.draw(); 
  for p in people: p.draw()

selectedActor = None

def on_mouse_down(pos): 
  global selectedActor
  for p in people:
    if p.collidepoint(pos): 
      selectedActor = p

def on_mouse_up(): 
  global selectedActor
  selectedActor = None

def on_mouse_move(rel):
  global selectedActor
  if selectedActor is not None: 
    dx, dy = rel
    x,  y  = selectedActor.pos
    x += dx; y += dy
    selectedActor.pos = (x,y)

### end ###
