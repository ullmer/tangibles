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
x, y, dx    = 40, 280, 250

eae = enoActorEnsemble()

for i in range(numBrackets):
  eae.addActor("b" + str(i), "tg01h2-bracket", pos=(x+i*dx, y))

ec   = enoContent()
etpe = enoThemePgzEnsemble()
etpe.loadEnoContent(ec, HEIGHT)
etpe.selectCursor()

def save(): print("save"); etpe.saveState()
def load(): print("load"); etpe.loadState()
def quit(): sys.exit()

x, y = 1550, 750; dy = 50
s = eae.addActor("save", "button_frame", pos=(x, y), text='save', cb=save, textOffset=(-52,-17)); y+=dy
l = eae.addActor("load", "button_frame", pos=(x, y), text='load', cb=load, textOffset=(-52,-17)); y+=dy
q = eae.addActor("quit", "button_frame", pos=(x, y), text='quit', cb=quit, textOffset=(-52,-17))

for el in [s,l,q]: el.selImgFn = 'button_frame_sel' #button frame, selected 

######################### draw #########################

def draw():
  screen.fill(BLACK)
  eae.draw(screen)
  etpe.draw(screen)

def on_mouse_down(pos): etpe.on_mouse_down(pos); eae.on_mouse_down(pos)
def on_mouse_move(rel): etpe.on_mouse_move(rel) 
def on_mouse_up(pos):   etpe.on_mouse_up();      eae.on_mouse_up()

def on_key_down(key):   etpe.on_key_down(key)
def on_key_up(key):     etpe.on_key_up(key)

#pgze = pgzEno(["multitouch"])
#pgze.go()

### end ###
