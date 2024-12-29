# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import pygame

from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesCsv import *

################### coursesPgz Categories ################### 

class CoursesCats(CoursesCsv):

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ################## error ##################

  def err(self, msg): print("CoursesPgzCats error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzCats msg:",   msg)

################## main ################## 

if __name__ == "__main__":
  cc = CoursesCats()

#def draw(): screen.clear(); cpgza.draw(screen)
#def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
