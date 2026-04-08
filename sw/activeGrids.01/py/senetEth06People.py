# Senet ethics example -- first example of classes
# Brygg Ullmer, Clemson University
# Begun 2026-03-25

from pgzero.builtins import Actor, animate, keyboard, keys

class senetEth06People:

  peopleAbbrev = ['gel', 'jgh', 'tr', 'fdr', 'er', 'rf']
  peoplePath   = "people/"
  people = None
  basePos = (300, 500)
  dx = 100
  selectedActor = None

  def __init__(self): self.buildActors()

  def buildActors(self):
    self.people = []
    x, y = self.basePos
    for pa in self.peopleAbbrev:
      imgFn = self.peoplePath + pa
      p = Actor(imgFn); self.people.append(p)
      p.pos = (x, y); x += self.dx 

  def draw(self): 
    for p in self.people: p.draw()

  def on_mouse_down(self, pos): 
    for p in self.people:
      if p.collidepoint(pos): 
        self.selectedActor = p

  def on_mouse_up(self): 
    animate(self.selectedActor, pos=(100,100), tween='accel_decel')
    self.selectedActor = None

  def on_mouse_move(self, rel):
    if self.selectedActor is not None: 
      dx, dy = rel
      x,  y  = self.selectedActor.pos
      x += dx; y += dy
      self.selectedActor.pos = (x,y)

### end ###
