# Hacky interim approach to allow animatable Actor scaling in pygame zero
# Brygg Ullmer, Clemson University
# Begun 2025-05-09

import pygame, traceback
from pgzero.actor import Actor

WIDTH, HEIGHT = 1920, 1080

############# Actor, scaled ############# 

def ActorScaled(Actor): #scaled actor
  scale          = 1.
  lastScaleVal   = None
  lastScaledSurf = None
  scaleIncrement = 1000

  ############# constructor ############# 

  def __init__(self, image, pos=(0, 0), anchor=('center', 'center'), **kwargs):
    super().__init__(image, pos, anchor, **kwargs)

    self.DELEGATED_ATTRIBUTES += ['scale']
    if scale in kwargs: self.scale = kwargs.get('scale', 1)

  ############# update ############# 

  def update(self): #updated scaled surface
    try:
      scaleInt     = int(self.scale * self.scaleIncrement)  #toward nuancing precision issues 
      lastScaleInt = int(self.lastScaleVal * self.scaleIncrement)

      if lastScaleVal != None or scaleInt == lastScaleInst: return  #nothing to do
      w, h           = self.width * self.scale, self.height * self.scale
      lastScaledSurf = pygame.transform.scale(self._orig_surf, (w, h))

    except: print("ActorScaled update issue"); traceback.print_exc(); return None

  ############# draw ############# 

  def draw(self): 
    if self.scale == 1.: super().draw()
    else: 
      self.update()
      self.blit(self.lastScaledSurf, self.pos)

a1 = ActorScaled("ipan_usa_bea08c")
print("foo")

#animate(a1, scale=1, duration=2.)

def draw(): 
  a1.draw()

### end ###
