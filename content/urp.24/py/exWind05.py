# Successive illustrative examples of local & distributed (second) Wind
# Brygg Ullmer, Clemson University
# Begun 2024-05-20

WIDTH, HEIGHT = 1920, 1080

import pgzSetup #move window to 0,0 / top-left of screen; determine if opacity supported
import math
from   enoWind import *

wind  = enoWind(opacitySupported=pgzSetup.opacitySupported)
bldg1 = Actor('wind21j-bldg3b', pos=(850, 450))
bldg2 = Actor('wind21s-bldg3b', pos=(350, 650))

actors       = [wind, bldg1, bldg2]
uiState      = {'current': None, 'translateActive': False, 'rotateActive': False,
                'translateFadeAnim': None, 'rotateFadeAnim': None}

#### draw ####

def draw(): 
  screen.clear()
  for a in actors:     a.draw()

#### mouse press ####

def on_mouse_down(pos): 
  for a in actors:
    if a.collidepoint(pos): 
      uiState['current'] = a
      if a == wind: wind.on_mouse_down(pos)

#### mouse release ####

def on_mouse_up():        
  uiState['lastActive'] = uiState['current']
  uiState['current']    = None
  wind.on_mouse_up()
    
#### mouse movement ####

def on_mouse_move(pos, rel):
  if uiState['current'] == wind:
    wind.on_mouse_move(pos, rel)
    return

  for a in actors:
    if uiState['current'] == a:
      dx, dy = rel
      x1, y1 = a.pos

      x2, y2 = x1+dx, y1+dy
      a.pos  = (x2, y2)

### end ###