# Approach to allow animatable Actor scaling in pygame zero
# Brygg Ullmer, Clemson University
# Begun 2025-05-09

import pygame, traceback

from enoActorScaled import *

WIDTH, HEIGHT = 1920, 1080

a1 = enoActorScaled("ipan_usa_bea08c")
a1.scale=.1

def grow():   animate(a1, scale=1,   duration=1.3, tween='accel_decel', on_finished=shrink)
def shrink(): animate(a1, scale=.05, duration=1.3, tween='accel_decel', on_finished=grow)

grow()

def draw(): screen.clear(); a1.draw()

### end ###
