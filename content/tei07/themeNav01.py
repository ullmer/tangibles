#New functionality warmup
#By Brygg Ullmer, Clemson University
#Begun 2023-12-08

import random, math
import pygame

from   enoThemePgz import *
from   enoContent  import *
from   pgzEno      import *

WIDTH  = 1600
HEIGHT = 1000
TITLE  = 'Enodia interactivity experiment'
BLACK  = (0, 0, 0)

winpos(0,0, WIDTH, HEIGHT) #provided by pgzEno; start window @0,0

numBrackets = 6
x, y = 40, 280
dx   = 250

eae = enoActorEnsemble()

for i in range(numBrackets):
  eae.addActor("b" + str(i), "tg01h2-bracket", pos=(x+i*dx, y))

eae.addActor("save", "button_frame", pos=(900, 900), text='save', textOffset=(-50,-10))

ec = enoContent()

c      = ec.tallyCountries()
kwDict = ec.tallyKeywords()
thPap  = ec.tallyThemes()

x,  y  = 130, 75
dy     = 100
y0     = y

etpe = enoThemePgzEnsemble()

for theme in thPap:
  papers = thPap[theme]
  kcount = len(ec.themesKeywords[theme])
  pcount = len(papers)
  #print("%s: K%i P%i" % (theme, kcount, pcount))
  etpe.addTheme(theme, kcount, pcount, "tg01h2-theme", pos=(x,y))
  y += dy
  if y > HEIGHT: y = y0; x += dx

######################### draw #########################

def draw():
  screen.fill(BLACK)
  eae.draw(screen)
  etpe.draw(screen)

def on_mouse_down(pos): etpe.on_mouse_down(pos)
def on_mouse_move(rel): etpe.on_mouse_move(rel)
def on_mouse_up(pos):   etpe.on_mouse_up()

#pgze = pgzEno(["multitouch"])
#pgze.go()

### end ###
