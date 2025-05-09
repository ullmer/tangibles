# Hacky interim approach to allow animatable Actor scaling in pygame zero
# Brygg Ullmer, Clemson University
# Begun 2025-05-09

import pygame, traceback

WIDTH, HEIGHT = 1920, 1080

a1   = Actor("ipan_usa_bea08c.png")
a1.scale = .1
print("FOO:", dir(a1))

a1sCache = {} # note that cache size management must still be handled 

def actorScale(actor, scale, actorScaleCacheDict):
  try:  
    scaleInt = int(scale*100) #toward nuancing precision issues 
    if scaleInt in actorScaleCacheDict: return actorScaleCacheDict[scaleInt] 

    origSurf   = actor._orig_surf
    w, h       = actor.width * scale, actor.height * scale
    scaledSurf = pygame.transform.scale(origSurf, (w, h))
    actorScaleCacheDict[scaleInt] = scaledSurf
    return scaledSurf

  except: print("actorScale issue"); traceback.print_exc(); return None

animate(a1, scale=1, duration=2.)

def draw(): 
  a1s = actorScale(a1, a1.scale, a1sCache)
  screen.blit(a1s, (0, 0))

### end ###
