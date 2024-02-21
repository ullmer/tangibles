# PyGame Zero examples 
# Brygg Ullmer, Clemson University 
# Begun 2022-11-01 

#https://pygame-zero.readthedocs.io/en/stable/

WIDTH  = 1024
HEIGHT = 1024

import moveWinHome #hack to move window to 0,0 on windows, avoiding redraw error

a1 = Actor("midjourney/homelessness-wall-01a")
a2 = Actor("midjourney/midjourney-figure-01b")

def draw():
  a1.draw()
  a2.draw()

### end ###
