# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import pygame

from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesCsv import *

################### coursesPgz Categories ################### 

class CoursesCats(Courses):

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ################## error ##################

  def err(self, msg): print("CoursesPgzCats error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzCats msg:",   msg)

  ################## get ##################

  def getCats(self): return self.cats

  def getNumCoursesInCat(self, cat): 
    if cat not in self.cats: self.msg("getNumCoursesInCats: cat not found: " + str(cat)); return None
    result = len(self.cats[cat])
    return result

  def getCoursesInCat(self, cat): 
    if cat not in self.cats: self.msg("getCoursesInCats: cat not found: " + str(cat)); return None
    result = self.cats[cat]
    return result

################## main ################## 

if __name__ == "__main__":
  cc = CoursesCats()
  cats = cc.getCats()
  for cat in cats:
    numCats = cc.getNumCoursesInCat(cat)
    print("%s: %i courses" % (cat, numCats))

#def draw(): screen.clear(); cpgza.draw(screen)
#def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
