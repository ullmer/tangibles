#Enodia Fargate animation illustrations
#By Brygg Ullmer, Clemson University
#Begun 2022-07-22

#Engages arc elements discussed here (with operationalization of the pillowa
# references therein yet to come)
#https://stackoverflow.com/questions/49346708/how-to-animate-arcs-in-python-pygame-zero

import random, math
import pygame
from   enoActor        import *
from   pgzEno          import *
from   pgzeSlider      import *
from   pgzero.builtins import Actor

WIDTH  = 510
HEIGHT = 310
TITLE  = 'Enodia interactors choreography designer'

BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
ORANGE = (255, 127, 0)

PI = math.pi

fg_delta = 0
wallBE = [20, 190] # beginning and ending X & Y coordinates of walls

w1, w2 = wallBE
wallRect = [10, 10, 290, 290]

eae = enoActorEnsemble()
eae.addActor("p1",        "person-iconic1",     pos=( 50, 50))
eae.addActor("addPerson", "person-add-iconic1", pos=(465, 55))

sr1Fn = "slider_glyph_rot01" # all of this should be external in YAML
sr2Fn = "slider_glyph_rot02"

sr1 = pgzeSlider([335, 155], sr1Fn) #slider : rotation 1 (orientation)
sr2 = pgzeSlider([390, 155], sr2Fn) #slider : rotation 2 (fargate ~shape)

eaa = enoActorArray("movements01.yaml")

widgets = [sr1, sr2]

cursorFn = "cursor1b"
cursors  = {}

######################### draw #########################

def draw():
  screen.fill(BLACK)
  #enFg(100, 100)
  enFg(102, 102) # coincides with an 8' section bent to 90 degrees

  for widget in widgets: widget.draw()
  eae.draw(screen)

  for finger_id in touch_coords:
    #pos   = touch_coords[finger_id]
    cursor = cursors[finger_id]
    cursor.draw()

######################### update #########################

def update():
  global fg_delta
  fg_delta += .3

##################### enodia fargate #####################

def enFg(w, h): #enodia fargate
  da = fg_delta * .1 #delta angle
  dp = fg_delta      #delta position

  #v1, v2 = wallBE[0],  wallBE[1]  #two values
  v1, v2 = wallBE[0] + dp,  wallBE[1] - dp #two values

  positions = []
  positions.append([v1, v1]) # top-left
  positions.append([v1, v2]) # top-right
  positions.append([v2, v2]) # bottom-right
  positions.append([v2, v1]) # bottom-left

  pygame.draw.rect(screen.surface, WHITE, wallRect, width=5) # 28' walls

  idx = 2 
  p1, a2 = PI/2 + da,  PI + da
  #p1, a2 = PI/2,  PI 

  for position in positions:
    x, y = position
    a3, a4 = p1 + idx*PI/2, a2 + idx*PI/2
    pygame.draw.arc(screen.surface, ORANGE, [x, y, w, h], a3, a4, width=5)
    idx += 1

############ finger events -- potentially multitouch ##########

touch_coords = {} # dictionary with coordinates of active touches
def normalizePos(x,y): return (int(x*WIDTH), int(y*HEIGHT))

############ fingerdown ##########

def on_finger_down(finger_id, x, y):
  pos    = touch_coords[finger_id] = normalizePos(x,y)
  cursor = Actor(cursorFn, pos)
  cursors[finger_id] = cursor

  px, py = x*WIDTH, y*HEIGHT

  eae.on_finger_down(finger_id, px, py)
  for widget in widgets: widget.on_finger_down(finger_id, px, py)

############ fingermove ##########

def on_finger_move(finger_id, x, y):
  on_finger_down(finger_id, x, y)

############ fingerup ##########

def on_finger_up(finger_id, x, y):
  print("finger UP")

################### "mouse" events ###################

def on_mouse_up(pos):
  #print("mouse UP")
  touch_coords.clear()

################### main ###################

pgze = pgzEno(["multitouch"])
pgze.go()

### end ###
