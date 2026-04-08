# ActiveGrid warmup
# Brygg Ullmer, Clemson University
# Begun 2026-03-24

import sys; sys.path.append("py") #support modules in py/ subdirectory

WIDTH, HEIGHT=1600,1100

from enoPeopleThemesYamlPgz import *

yfn = 'yaml/peopleThemes03.yaml'

a    = Actor('backdrops/senet03k')
epyp = EnoPeopleYamlPgz()
epyp.loadYaml(yfn)
epyp.buildActors()

def draw():             a.draw(); epyp.draw()
def on_mouse_down(pos): epyp.on_mouse_down(pos)
def on_mouse_up():      epyp.on_mouse_up()
def on_mouse_move(rel): epyp.on_mouse_move(rel)

#pgzrun.go()

### end ###
