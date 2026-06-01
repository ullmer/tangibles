# Enodia prisms manuscripts browser
# Brygg Ullmer, Clemson University
# Begun 2025-11-03

import os, sys
from pgzero import clock

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0' #place window at 0,0 
sys.path.insert(0, #access module in parent directory (for test stubs)
  os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pgzrun, yaml
from pgzero.builtins import Actor, animate, keyboard, keys

WIDTH, HEIGHT=1800,1080

from enoPrisms        import *
from enoRefractBar    import *
from enoFrameBox      import *
from enoEntityListing import *
from enoCursorBox     import *

##### main ##### 

ep = EnoPrisms()
ep.summonPrism('teiLandscape', 0)
ep.summonPrism('teiYearsQ4',   1)

winDim = (WIDTH, HEIGHT)

yf  = open('yaml/sampleEntries.yaml', 'rt')
yd  = yaml.safe_load(yf); yf.close()
eel = EnoEntityListing(entries=yd, fieldsToPostfix=[0],
                       entryFontSize=25, winDim=winDim)

rb  = EnoRefractBar((WIDTH, 80), (0, 750))
ecb = EnoCursorBox(dim=(10, 10), width=4)

def update(): ep.update(); 

firstDraw = True

def initPrismBarPairIntersect(): ep.intersectPrismBarPair(0, 1, 0, 0)
clock.schedule_unique(lambda: initPrismBarPairIntersect(), 0) 

tfn = "barlow_black"

################ draw ################
def draw(): 
  screen.clear()
  for el in [eel, ep, rb, ecb]: el.draw(screen)
  rcol = rb.fillColor
  screen.draw.text("TEI", midleft=(305,70), alpha=.2, color=rcol, fontname=tfn, fontsize=250)

################ on_mouse/key_down ################

def on_mouse_down(pos):    barId = ep.evolveLocus(pos, ecb)
def on_key_down(key, mod): ecb.on_key_down(key, mod)

pgzrun.go()

### end ###
