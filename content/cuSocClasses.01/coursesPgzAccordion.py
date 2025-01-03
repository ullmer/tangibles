# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import pygame

from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesPgzBase    import *

################### coursesPg ################### 

class CoursesPgzAccordion(CoursesPgzBase):

  plsDraw2 = False #copilot asserts that this overriding of CoursePgzBase's class variable defaults
  plsDraw3 = True

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

  ################## error ##################

  def err(self, msg): print("CoursesPgzAccordion error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzAccordion msg:",   msg)

  ################## draw ##################

  def draw(self, screen): 
    super().draw(screen)
    if self.plsDraw3: self.draw3(screen)

  ################## draw samples #3 ##################

  def draw3(self, screen): 

    colorIndices = [3,1,2,0]

    bds = [] #backdrops/backgrounds of individual courses, across several colors
    for i in colorIndices: bds.append(self.divisionBackdropA[i])

    dcs = [] # toward colorbars. refactor next line & above
    for i in colorIndices: dcs.append(self.divColors[i]) 

    x0     = self.x0b  #refactor names
    cats   = self.getCats(); colIdx = 0

    for cat in cats: #first, work through categories
      courses = self.getCoursesInCat(cat); y0 = self.y0b
      self.drawCourses2(screen, courses, x0, y0, bds, dcs)
      x0 += self.dx

    littleDivs = self.actorCats; bigDivs    = []
    for div in littleDivs: divUp = div.upper(); bigDivs.append(divUp)

    for divBig in bigDivs: #next, work through divisions
      courses = self.getCourseByDiv(divBig); y0 = self.y0b
      self.drawCourses2(screen, courses, x0, y0, bds, dcs)
      x0 += self.dx
  
  ################## draw samples #1 ##################

  def drawCourses3(self, screen, courses, x0, y0, bds, dcs): 
    courseIdx, barIdx = 0, 0
        
    for courseID in courses:
      div    = self.mapCourseToDivisions(courseID)
      if div is None: self.msg("drawSamples2: ignoring null div"); continue

      divLow = div.lower()
      if divLow in self.actorCats: divIdx = self.actorCats.index(divLow)
      else:                        self.msg("drawSamples2: ignoring div issue: " + str(divLow)); continue
      backdrop = bds[divIdx]; barColor=dcs[divIdx]

      if courseIdx < 4: 
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
