# Successive illustrative examples of local & distributed (second) Wind
# Brygg Ullmer, Clemson University
# Begun 2024-05-20

WIDTH, HEIGHT = 1920, 1080
import pgzSetup
import pygame
import math

w       = Actor('wind21e3')
touched = {'current': None}

#### draw ####

def draw(): 
  screen.clear()
  w.draw()
  #r = Rect(100, 100, 200, 200)
  r = Rect(300, 300, 600, 600)
  v = 100
  pygame.draw.arc(screen.surface, (v,v,v), r, 0, math.pi/2, 20)

#### handle simplest interactivity ####

def on_mouse_up():        touched['current'] = None

def on_mouse_down(pos): 
  if w.collidepoint(pos): touched['current'] = 'wind'

def on_mouse_move(rel):
  dx, dy = rel

  if touched['current'] == 'wind':
    x1, y1 = w.pos
    x2, y2 = x1+dx, y1+dy
    w.pos  = (x2, y2)

### end ###
