#New functionality warmup
#By Brygg Ullmer, Clemson University
#Begun 2023-12-08

import random, math
import pygame
from   enoActor        import *
from   pgzEno          import *
from   pgzero.builtins import Actor

WIDTH  = 1024
HEIGHT = 768
TITLE  = 'Enodia interactivity experiment'
BLACK  = (0, 0, 0)

eae = enoActorEnsemble()
a1 = eae.addActor("t1", "tg01h2-theme", pos=(200, 100))
a2 = eae.addActor("t2", "tg01h2-theme", pos=(200, 300))

a1.textPrimary = 'foo'
a2.textPrimary = 'supercalifragilistic'

a1.primaryTextOffset = (-60, -40)

######################### draw #########################

def draw():
  screen.fill(BLACK)
  eae.draw(screen)

touch_coords = {} # dictionary with coordinates of active touches
def normalizePos(x,y): return (int(x*WIDTH), int(y*HEIGHT))

############ fingerdown ##########

def on_finger_down(finger_id, x, y):
  pos    = touch_coords[finger_id] = normalizePos(x,y)
  cursor = Actor(cursorFn, pos)
  cursors[finger_id] = cursor

  px, py = x*WIDTH, y*HEIGHT

  eae.on_finger_down(finger_id, px, py)

pgze = pgzEno(["multitouch"])
pgze.go()

### end ###
