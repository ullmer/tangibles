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

  #copilot: "The first known computer game to make extensive use of alphanumeric key bindings for controlling 
  #          on-screen character movement and actions is "Rogue", developed in 1980."
  #map "q" to column 0, up, etc.; old keyboard-driven 1980s game-style

  keyDict = {'q': "0U", "w": "1U", "e": "2U", 'r': "3U", 't': "4U", 'y': "5U", 'u': "6U", 'i': "7U", 'o': "8U",
             'a': "OD", "s": "1D", "d": "2D", 'f': "3D", 'g': "4D", 'h': "5D", 'j': "6D", 'k': "7D", 'l': "8D"}

  keyCodeDict = None

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
    self.keyCodeDict = {}

    for key in self.keyDict:
      val = self.keyDict[key]; upkey = key.upper()
      keycode = keys[upkey]
      self.keyCodeDict[keycode] = val

  ################## on key down##################

  def on_key_down(self, key):
    if self.keyCodeDict is None:    self.msg("on_key_down: keyCodeDict not initialized!");       return
    if key not in self.keyCodeDict: self.msg("on_keh_down: key not in dictionary: " + str(key)); return

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
