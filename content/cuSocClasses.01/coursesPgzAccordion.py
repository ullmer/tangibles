# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import pygame

from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesPgzBase    import *

################### coursesPg ################### 

class CoursesPgzAccordion(CoursesPgzBase):

  colDisplayIndexDict = None

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.selectedDrawCoursesFunc = self.drawCourses3

    self.initColDisplayIndexDict()

  ################## error ##################

  def err(self, msg): print("CoursesPgzAccordion error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzAccordion msg:",   msg)

  ################## initialize col diplsay indices dict ##################

  def initColDisplayIndexDict(self):

    self.colDisplayIndexDict = {}

  ################## draw samples #1 ##################

  def drawCourses3(self, screen, courses, x0, y0, bds, dcs): 
    self.msg("drawCourses3")

    courseIdx, barIdx = 0, 0
    numCourses = len(courses)
        
    for courseID in courses:
      div    = self.mapCourseToDivisions(courseID)
      if div is None: self.msg("drawCourses3: ignoring null div"); continue

      divLow = div.lower()
      if divLow in self.actorCats: divIdx = self.actorCats.index(divLow)
      else:                        self.msg("drawCourses3: ignoring div issue: " + str(divLow)); continue
      backdrop = bds[divIdx]; barColor=dcs[divIdx]

      #if courseIdx < 4: 
      if courseIdx > numCourses-5:
        backdrop.topleft=(x0, y0); backdrop.draw()
        self.drawCourse(screen, courseID, x0, y0, barColor)
        y0 += self.dy1
      else: 
        self.drawCourseBar(screen, courseID, x0, y0, barColor); 
        barIdx += 1
        if barIdx % 4: y0 += self.barDy1
        else:          y0 += self.barDy2

      courseIdx += 1

################## main ################## 

#if __name__ == "__main__":

cpgza = CoursesPgzAccordion()

def draw(): screen.clear(); cpgza.draw(screen)
def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
