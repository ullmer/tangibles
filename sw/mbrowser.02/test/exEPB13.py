# Enodia "prism bars"
# Brygg Ullmer, Clemson University
# Begun 2025-11-03

import os,sys

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0' #place window at 0,0 
sys.path.insert(0, #access module in parent directory (for test stubs)
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sys.path.append('..')

import pgzrun
WIDTH, HEIGHT=1900,1000

from enoPrismBar  import *
from enoPrismBars import *

##### main ##### 

color1  = (0, 0, 255, 80)
color2  = (255, 255, 0, 60)

epb2 = EnoPrismBars(flowLeft=True, textOffset2=(350, 0))
b2   = epb2.addBar("bar1", color2, 150)
b3   = epb2.addBar("bar2", color2, 160)

b2.qx = 200

epb = [epb2]

def draw(): 
  screen.clear()
  for p in epb: p.draw(screen)

def animBar(nudge): 
  print("animate bar")
  #b2.shiftBarWidth(nudge)
  b2.shiftBarTX(nudge)

def addBar(): 
  print("add bar")
  epbn = EnoPrismBars(flowLeft=True, textOffset2=(350, 0))
  epbn.addBar("bar1", color2, 200)
  epb.append(epbn)

################ on_mouse/key_down ################

def on_mouse_down(pos):    barId = ep.evolveLocus(pos, ecb)

def on_key_down(key, mod): 
  if keyboard.left:  b2.qx -= 200; animBar(b2.qx)
  if keyboard.right: b2.qx += 200; animBar(b2.qx)

#def on_key_down(key, mod): addBar()

pgzrun.go()

### end ###
