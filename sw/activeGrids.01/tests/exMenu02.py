# https://pygame-zero.readthedocs.io/en/stable/ptext.html
# https://pythonprogramming.altervista.org/pygame-4-fonts/

import sys; sys.path.append("py") # import modules from py/ subdirectory 
from enoAnimistHomeMenu import *

WIDTH, HEIGHT = 900, 900

eahm = EnoAnimistHomeMenu(yamlFn = "yaml/animistHomeMenu01.yaml", requestAnim=True)

def draw(): screen.clear(); eahm.draw(screen)
def on_mouse_down(pos):     eahm.on_mouse_down(pos)

### end ###
