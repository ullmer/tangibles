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
  colDispWindowDefaultSize = 4 #default number of courses that we have room to textually display

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

  def nudgeCol(self, whichColInt, whichDir):
    if self.colDisplayIndexDict is None: self.msg("nudgeCol: column display index not initialized"); return
    if self.colNamesList        is None: self.msg("nudgeCol: column names list not initialized");    return

    cnl     = self.getColNames()
    numCols = len(cnl)
 
    if whichColInt < 0 or whichColInt >= numCols: self.msg("nudgeCol: column index issue: " + str(whichColInt)); return
    colName    = cnl[whichColInt]
    colNameVal = self.colDisplayIndexDict[colName]
    colLen     = self.getColLenByIdx(whichColInt)
  
    cdwds = self.colDispWindowDefaultSize 

    if    colLen > 0 and whichDir == 'D':                  self.colDisplayIndexDict[colName] -= 1
    elif  colNameVal < colLen - cdwds and whichDir == 'U': self.colDisplayIndexDict[colName] += 1 
    else: self.msg("nudgeCol: problematics"); return
    
  ################## on key down##################

  def on_key_down(self, key):
    if self.keyCodeDict is None:    self.msg("on_key_down: keyCodeDict not initialized!");       return
    if key not in self.keyCodeDict: self.msg("on_keh_down: key not in dictionary: " + str(key)); return

    self.msg("on_key_down " + str(key))

    val = self.keyCodeDict[key]

    try:
      whichColCh = val[0] #use try-except to "more efficiently" catch all errors
      whichDir   = val[1]

      whichColInt = int(whichColCh)
      self.nudgeCol(whichColInt, whichDir)

    except: self.err("on_key_down " + str(key))

  ################## initialize col diplsay indices dict ##################

  def initColDisplayIndexDict(self):

    self.colDisplayIndexDict = {}
    nc = self.getNumColumns()
    for colIdx in range(nc): self.colDisplayIndexDict[colIdx] = 0 #default to beginning

    #colNamesList = self.getColNames()
    #for colName in colNamesList: self.colDisplayIndexDict[colName] = 0 #default to beginning

  ################## get column display index ################## 

  def getColDisplayIndex(self, whichCol):
    if self.colDisplayIndexDict is None: 
      self.msg("getColDisplayIndex: index dictionary not initialized"); return None

    if whichCol not in self.colDisplayIndexDict: 
      self.msg("getColDisplayIndex: specified column has issue: " + str(whichCol)); return None

    result = self.colDisplayIndexDict[whichCol]
    return result

  ################## draw samples #1 ##################

  def drawCourses3(self, screen, courses, x0, y0, bds, dcs, whichCol): 
    courseIdx, barIdx = 0, 0
    numCourses = len(courses)
    cdwds      = self.colDispWindowDefaultSize #default number of courses that we have room to textually display

    colIdx = self.getColDisplayIndex(whichCol) #column index
    if colIdx is None: self.msg("drawCourses3: column index unassigned for column " + str(whichCol)); return None
        
    for courseID in courses:
      div    = self.mapCourseToDivisions(courseID)
      if div is None: self.msg("drawCourses3: ignoring null div"); continue

      divLow = div.lower()
      if divLow in self.actorCats: divIdx = self.actorCats.index(divLow)
      else:                        self.msg("drawCourses3: ignoring div issue: " + str(divLow)); continue
      backdrop = bds[divIdx]; barColor=dcs[divIdx]

      #if courseIdx < 4: 
      #if courseIdx > numCourses-5:
      if courseIdx >= colIdx and courseIdx <= colIdx + cdwds: #shape the window

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
def on_key_down(key):       cpgza.on_key_down(key)
def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
