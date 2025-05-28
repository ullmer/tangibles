# Approach to allow animatable Actor scaling in Pygame Zero
# Brygg Ullmer, Clemson University
# Begun 2025-05-09

import pygame, traceback
from pgzero.actor import Actor

#WIDTH, HEIGHT = 1920, 1080

############# Actor, scaled ############# 

class enoActorScaled(Actor): #scaled actor
  scale          = 1.
  lastScaleVal   = 1.
  lastScaledSurf = None
  scaleIncrement = 1000

  ############# constructor ############# 

  def __init__(self, image, pos=None, anchor=None, **kwargs):
    self.__dict__.update(kwargs) 
    super().__init__(image, pos, anchor)

  ############# update ############# 

  def updateScale(self): #updated scaled surface
    try:
      scaleInt     = int(self.scale * self.scaleIncrement)  #toward nuancing precision issues 
      lastScaleInt = int(self.lastScaleVal * self.scaleIncrement)

      if scaleInt == lastScaleInt: return  #nothing to do
      w, h                = self.width * self.scale, self.height * self.scale
      self.lastScaledSurf = pygame.transform.scale(self._orig_surf, (w, h))

    except: print("ActorScaled update issue"); traceback.print_exc(); return None

  ############# draw ############# 

  def draw(self, screen): 
    screen.clear()
    if self.scale == 1.: super().draw()
    else: 
      self.updateScale()
      if self.lastScaledSurf is None:
        print("ActorScaled draw: unexpected error with last scaled surface")
      else:
        #screen.blit(self.lastScaledSurf, self.pos)
        screen.blit(self.lastScaledSurf, self.topleft)

#a1 = enoActorScaled("ipan_usa_bea08c")
#a1.scale=.1

#def grow():   animate(a1, scale=1,  duration=1.5, tween='accel_decel', on_finished=shrink)
#def shrink(): animate(a1, scale=.1, duration=1.5, tween='accel_decel', on_finished=grow)

#grow()

#def draw(): 
#  a1.draw()

### end ###
