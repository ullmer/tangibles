#New functionality warmup
#By Brygg Ullmer, Clemson University
#Begun 2023-12-08

import random, math
import pygame

from   enoThemePgz import *
from   enoContent  import *

from   pgzEno          import *
from   pgzero.builtins import Actor

WIDTH  = 1600
HEIGHT = 768
TITLE  = 'Enodia interactivity experiment'
BLACK  = (0, 0, 0)

winpos(0,0, WIDTH, HEIGHT) #provided by pgzEno

etpe = enoThemePgzEnsemble()
a1 = etpe.addTheme("foo",    3, 5, "tg01h2-theme", pos=(200, 100))
a2 = etpe.addTheme("swishy", 5, 9, "tg01h2-theme", pos=(200, 300))

numBrackets = 6
x, y = 50, 300
dx   = 250

eae = enoActorEnsemble()

for i in range(numBrackets):
  eae.addActor("b" + str(i), "tg01h2-bracket", pos=(x+i*dx, y))

ec = enoContent()

c      = ec.tallyCountries()
kwDict = ec.tallyKeywords()
thPap  = ec.tallyThemes()

for theme in thPap:
  papers = thPap[theme]
  kcount = len(ec.themesKeywords[theme])
  pcount = len(papers)
  print("%s: K%i P%i" % (theme, kcount, pcount))

######################### draw #########################

def draw():
  screen.fill(BLACK)
  eae.draw(screen)
  etpe.draw(screen)

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
