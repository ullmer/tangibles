#Theme navigator GUI
#By Brygg Ullmer, Clemson University
#Begun 2023-12-08

import pygame, sys

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

ec   = enoContent()
etpe = enoThemePgzEnsemble()

def save(): print("save"); etpe.saveState()
def load(): print("load")
def quit(): sys.exit()

x, y = 1550, 750; dy = 50
s = eae.addActor("save", "button_frame", pos=(x, y), text='save', cb=save, textOffset=(-52,-17)); y+=dy
l = eae.addActor("load", "button_frame", pos=(x, y), text='load', cb=load, textOffset=(-52,-17)); y+=dy
q = eae.addActor("quit", "button_frame", pos=(x, y), text='quit', cb=quit, textOffset=(-52,-17))

for el in [s,l,q]: el.selImgFn = 'button_frame_sel' #button frame, selected 

c      = ec.tallyCountries()
kwDict = ec.tallyKeywords()
thPap  = ec.tallyThemes()

x,  y  = 130, 75
dy     = 100
y0     = y

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

def on_mouse_down(pos): etpe.on_mouse_down(pos); eae.on_mouse_down(pos)
def on_mouse_move(rel): etpe.on_mouse_move(rel) 
def on_mouse_up(pos):   etpe.on_mouse_up();      eae.on_mouse_up()

#pgze = pgzEno(["multitouch"])
#pgze.go()

### end ###
