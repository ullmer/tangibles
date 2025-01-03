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

  keyDict             = None

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.selectedDrawCoursesFunc = self.drawCourses3

    self.initColDisplayIndexDict()
    self.bindKeys()

  ################## error ##################

  def err(self, msg): print("CoursesPgzAccordion error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzAccordion msg:",   msg)

  ################## bind keys ##################

  def bindKeys(self):
    self.keyDict = {}

    k = keyboard

    #copilot: "The first known computer game to make extensive use of alphanumeric key bindings for controlling 
    #          on-screen character movement and actions is "Rogue", developed in 1980."

    #The below could all be done more compactly, and perhaps should; but not immediately clear it would assist legibility

    self.keyDict[k.q] = "0U" #map "q" to column 0, up; old keyboard-driven 1980s game-style
    self.keyDict[k.a] = "0D" #map "a" to column 0, down
    self.keyDict[k.w] = "1U" #map "w" to column 1, up
    self.keyDict[k.s] = "1D" #map "s" to column 1, down
    self.keyDict[k.e] = "2U" #map "e" to column 2, up
    self.keyDict[k.d] = "2D" #map "d" to column 2, down

    self.keyDict[k.r] = "3U" #map "r" to column 3, up; old keyboard-driven 1980s game-style
    self.keyDict[k.f] = "3D" #map "f" to column 3, down
    self.keyDict[k.t] = "4U" #map "t" to column 4, up
    self.keyDict[k.g] = "4D" #map "g" to column 4, down
    self.keyDict[k.y] = "5U" #map "y" to column 5, up
    self.keyDict[k.h] = "5D" #map "h" to column 5, down

    self.keyDict[k.u] = "6U" #map "u" to column 6, up; old keyboard-driven 1980s game-style
    self.keyDict[k.j] = "6D" #map "j" to column 6, down
    self.keyDict[k.i] = "7U" #map "i" to column 7, up
    self.keyDict[k.k] = "7D" #map "k" to column 7, down
    self.keyDict[k.o] = "8U" #map "o" to column 8, up
    self.keyDict[k.l] = "8D" #map "l" to column 8, down

  ################## initialize col diplsay indices dict ##################

  def initColDisplayIndexDict(self):

    self.colDisplayIndexDict = {}
    colNamesList = self.getColNames()
    
    for colName in colNamesList: self.colDisplayIndexDict[colName] = 0 #default to beginning

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
