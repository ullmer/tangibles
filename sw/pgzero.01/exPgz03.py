# PyGame Zero examples 
# Brygg Ullmer, Clemson University 
# Begun 2022-11-01 

#https://pygame-zero.readthedocs.io/en/stable/

WIDTH  = 1358
HEIGHT = 1024

import moveWinHome #hack to move window to 0,0 on windows, avoiding redraw error

a1 = Actor("midjourney/homelessness-wall-01b")
a2 = Actor("midjourney/midjourney-figure-01b", pos=(100,550))
a3 = Actor("as_unit/as_unit_01b2",              pos=(400,450))
#a3 = Actor("as_unit/as_unit_01d",              pos=(400,450))

actors = [a1, a3, a2]

def draw():
  for actor in actors: 
    actor.draw()

### end ###
