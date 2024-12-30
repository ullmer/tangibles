# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import pygame

from socDb import * #school of computing database
from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesCsv import *

################### coursesPgz Categories ################### 

class CoursesCats(Courses):
  socDbInst       = None

  instructors     = None
  faculty2div     = None
  div2faculty     = None

  mapCourse2Div   = None
  mapDiv2Courses  = None
  mapCourse2Title = None

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

    self.socDbInst = socDb()
    self.mapInstructorsC2S()
    self.mapCourseInstructorsToDivisions()
    self.mapCoursesToDivisions()

  ################## error ##################

  def err(self, msg): print("CoursesPgzCats error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgzCats msg:",   msg)

  ################## get ##################

  #def getCats(self): return list(self.catsDict.keys())
  def getCats(self): return self.cats

  def getNumCoursesInCat(self, cat): 
    if cat not in self.catsDict: self.msg("getNumCoursesInCats: cat not found: " + str(cat)); return None
    result = len(self.catsDict[cat])
    return result

  def getCoursesInCat(self, cat): 
    if cat not in self.catsDict: self.msg("getCoursesInCats: cat not found: " + str(cat)); return None
    result = self.catsDict[cat]
    return result #returns a list

  def getCoursesInCatStr(self, cat):  
    coursesList = self.getCoursesInCat(cat)
    if coursesList is None: self.msg("getCoursesInCatStr: noted problem for cat " + str(cat)); return None

    result = ' '.join(coursesList)
    return result

  ############# extract field values unique #############

  def extractFieldValsUnique(self, fieldName):
    try:
      vals = self.extractFieldVals(fieldName)
      if vals is False: return False
    
      result = []
      for val in vals:
        if val not in result: result.append(val)
      return result
    except:
      self.err("extractFieldValsUnique exception")
      traceback.print_exc(); return False

  ############# getInstructors #############

  def getInstructors(self):
    instr1 = self.extractFieldValsUnique('Instructor') #first, get raw fields
    instr2 = []; postfix1 = ' (P)'; postfix2 = ' (GTR)'
    self.mapNameR2C  = {}

    for instr in instr1:
      if   instr.find(postfix1) > -1: instrCl = instr[:-4]; instr2.append(instrCl) #instructor-clean
      elif instr.find(postfix2) > -1: instrCl = instr[:-6]; instr2.append(instrCl) #instructor-clean
      else:                           instrCl = instr; instr2.append(instr)

      self.mapNameR2C[instr] = instrCl

    instr2.sort()
    return instr2

  ############# mapInstructorsC2S (map in csv to sql; middle name inclusion inconsistent) #############

  def mapInstructorsC2S(self):
    result  = {}
    instr1  = self.getInstructors()
    instr2P = self.socDbInst.getFaculty()
    instr2  = list(instr2P['name'])

    self.mapNameR2D = {}
    self.mapNameC2D = {}
    self.mapNameD2C = {}

    for instr in instr1: 
      if instr in instr2: self.mapNameC2D[instr] = instr; #print(">", instr)
      else:
        instrFields = instr.split(' ')
        instrFirst  = instrFields[0]
        instrLast   = instrFields[-1]
        instrFL     = instrFirst + " " + instrLast

        if instrFL  in instr2: 
          self.mapNameC2D[instr]   = instrFL
          self.mapNameD2C[instrFL] = instr

    #print("instr1: ", instr1)
    #print("instr2: ", instr2)

  ############# mapCourseInstructorsToDivisions #############

  def getCourseByDiv(self, divSpecified=None):
    result = []

    if divSpecified is None:
      try:
        divisions = self.socDbInst.getDivisions()
        for div in divisions:
          r2 = self.getCoursesByDiv(div); result += r2
      except:
        self.err("getCoursesByDiv exception on unspecified division")
        traceback.print_exc(); return False
    else: 
      for row in self.rowtableRows:
        subject, course, instr = row['Subj'], row['Crse'], row['Instructor']
        instr2 = self.mapNameC2D[instr] 

  ############# mapCourseInstructorsToDivisions #############

  def mapCourseInstructorsToDivisions(self):
    self.instructors = []
    self.faculty2div = {}
    self.div2faculty = {}

    try:
      for instr1 in self.mapNameC2D: self.instructors.append(self.mapNameC2D[instr1])

      instrDF = self.socDbInst.getFaculty()
      for index, row in instrDF.iterrows():
        faculty, division = row['name'], row['division']
        self.faculty2div[faculty]  = division
        if division not in self.div2faculty: self.div2faculty[division] = []
        self.div2faculty[division].append(faculty)
    except:
      self.err("mapCourseInstructorsToDivisions exception")
      traceback.print_exc(); return False

  ############# mapCourseInstructorsToDivisions #############

  def mapCoursesToDivisions(self):
    self.mapCourse2Div   = {}
    self.mapDiv2Courses  = {}
    self.mapCourse2Title = {}

    try:
      for row in self.tableRows:
        print("foo", row)
        subject, course1, instructor, title, mode = row[0], row[1], row[10], row[5], row[3]
        if mode == 'CRSRA': continue #skip Coursera for the moment; interesting to consider converse
        course2  = subject + course1
        name1    = self.mapNameR2C[instructor]
        name2    = self.mapNameC2D[name1]
        division = self.faculty2div[name2]
        #print(course2, name2, division)

        if division not in self.mapDiv2Courses: self.mapDiv2Courses[division] = []
        self.mapCourse2Div[course2]   = division
        self.mapCourse2Title[course2] = title
        if course2 not in self.mapDiv2Courses[division]: 
          self.mapDiv2Courses[division].append(course2)

################## main ################## 

if __name__ == "__main__":
  cc = CoursesCats()
  cats = cc.getCats()
  #print("catsDict:" + str(cc.catsDict))
  for cat in cats:
    numCats = cc.getNumCoursesInCat(cat)
    courses = cc.getCoursesInCatStr(cat)
    print("%s: %i courses" % (cat, numCats))
    print(">> " + courses)

#def draw(): screen.clear(); cpgza.draw(screen)
#def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
