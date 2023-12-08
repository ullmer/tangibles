#New functionality warmup
#By Brygg Ullmer, Clemson University
#Begun 2023-12-08

import random, math
import pygame
from   enoActor        import *
from   pgzEno          import *
from   pgzero.builtins import Actor

WIDTH  = 510
HEIGHT = 310
TITLE  = 'Enodia interactivity experiment'
BLACK  = (0, 0, 0)

eae = enoActorEnsemble()
a1 = eae.addActor("p1",        "person-iconic1",     pos=( 50, 50))
a2 = eae.addActor("addPerson", "person-add-iconic1", pos=(465, 55))

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
