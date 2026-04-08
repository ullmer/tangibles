# Senet ethics example
# Brygg Ullmer, Clemson University
# Begun 2026-03-24

WIDTH, HEIGHT=1535,1180

from senetEth06People import *

a  = Actor('backdrops/senet03k')
se6p = senetEth06People()

def draw(): a.draw(); se6p.draw()

def on_mouse_down(pos): se6p.on_mouse_down(pos)
def on_mouse_up():      se6p.on_mouse_up()
def on_mouse_move(rel): se6p.on_mouse_move(rel)

### end ###
