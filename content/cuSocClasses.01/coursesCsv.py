# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2024-09-05
# Evolution begun  2024-12-25

import csv, traceback
from courseBase import *

################## Courses class ##################

class Courses: #not catching any errors; caveat emptor
  fnMain             = 'S25.csv'        #filename
  fnAbbrev           = 'S25abbrev.csv'  #filename
  csvDMain           = None             #CSV data
  csvDAbbrev         = None             
  csvHeaderFieldsM   = None
  csvHeaderFieldsA   = None
  coursesDict        = None
  courseIdsByPrefix  = None
  numCourseGroups    = 0
  verbose            = False
  instrPostfix1      = ' (P)'; 
  instrPostfix2      = ' (GTR)'
  cats               = ['apps', 'core', 'graphics', 'hw', 'interaction'] #categories
  catsDict           = None
  catAssocChars      = ['*', ':'] # initially, *=primary, :=secondary; but init. folding together

  ################## constructor, err ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.loadCsv()
  
  def err(self, msg): print("Courses error:", msg); traceback.print_exc()
  def msg(self, msg): print("Courses msg:",   msg)

  def size(self): 
    if self.coursesDict is None: return 0
    cdkl = list(self.coursesDict.keys())
    return len(cdkl)

  ################## load YAML from file ##################

  def loadCsv(self): 
    self.coursesDict       = {}
    self.courseIdsByPrefix = {}
    self.catsDict          = {}
    for cat in self.cats: self.catsDict[cat] = [] #list of course IDs associated with each category

  ################## constructor, err ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.loadCsv()
  
  def err(self, msg): print("Courses error:", msg); traceback.print_exc()
  def msg(self, msg): print("Courses msg:",   msg)

  def size(self): 
    if self.coursesDict is None: return 0
    cdkl = list(self.coursesDict.keys())
    return len(cdkl)

  ################## load YAML from file ##################

  def loadCsv(self): 
    self.coursesDict       = {}
    self.courseIdsByPrefix = {}
    self.catsDict          = {}

    try:
      f        = open(self.fnMain, 'rt')  
      rdr      = csv.reader(f, delimiter=',', quotechar='"')
      firstRow = True

      ipf1, ipf2 = self.instrPostfix1, self.instrPostfix2 

      for row in rdr:   ### Process main file
        if firstRow: self.processCsvHeaderMain(row); firstRow = False; continue
        c = Course()
        c.setFields(self.csvHeaderFields, row)

        crse = c.getField('Crse')
        if crse.find('4+6') > -1: crse2 = 'x' + crse[3:]; c.setField('Crse', crse2)
        courseId = c.getCourseId()

        instr1 = c.getField('Instructor')
        if   instr1.find(ipf1) > -1: instr2 = instr1[:-4]; c.setField('Instructor', instr2)
        elif instr1.find(ipf2) > -1: instr2 = instr1[:-6]; c.setField('Instructor', instr2)

        instr1 = c.getField('InstructorTrunc')
        if   instr1.find(ipf1) > -1: instr2 = instr1[:-4]; c.setField('InstructorTrunc', instr2)
        elif instr1.find(ipf2) > -1: instr2 = instr1[:-6]; c.setField('InstructorTrunc', instr2)

        self.coursesDict[courseId] = c

        subj = c.getField('Subj')
        if subj not in self.courseIdsByPrefix: self.courseIdsByPrefix[subj] = []
        self.courseIdsByPrefix[subj].append(courseId)

      f.close()

      f        = open(self.fnAbbrev, 'rt') # Read abbrev file next
      rdr      = csv.reader(f, delimiter=',', quotechar='"')
      firstRow = True

      for row in rdr:   ### Process abbreviations file
        if firstRow: firstRow = False; continue
   
        try:
          subject, course, abbrev = row[0:3]

          courseID = subject + course
          c = self.getCourseById(courseID)
          if c is None: self.msg("loadCsv: problem in assigning abbrev to " + courseId)
          else: 
            c.setField('abbrevTitle', abbrev)
            a,c,g,h,i = row[4:] # applications,core,graphics,hardware,interaction #hacky, but time-pressed

            c.cats = self.cats
            c.setFields(c.cats, [a,c,g,h,i])


        except: self.err("loadCsv abbrev issue")
    except: self.err("loadCsv issue")

  ################## process CSV header ##################

  def processCsvHeaderMain(self, row): 
    self.csvHeaderFields     = row 
    self.csvHeaderFieldsDict = {}
    idx = 0
   
    for field in row:
      self.csvHeaderFieldsDict[field] = idx
      idx += 1

  ################## print course IDs ##################

  def printCourseIds(self): 
    try:
      nc = self.getNumCourses()
      for i in range(nc):
        c = self.getCourseByIdx(i); c.printCourseId()
    except: self.err("printCourseIds issue")

  ################## get number of courses ##################

  def getNumCourses(self): 
    try:
      cidList = list(self.coursesDict.keys())
      return len(cidList)
    except: self.err("getNumCourses issue:")

  ################## get course by idx ##################

  def getCourseById(self, courseId): 
    try:
      if courseId in self.coursesDict: return self.coursesDict[courseId]
      return None
      
    except: self.err("getCourseById issue: " + courseId); return

  ################## get course by idx ##################

  def getCourseIdByIdx(self, i): 
    try:
      coursesL = list(self.coursesDict)
      result = coursesL[i]
      return result
    except: self.err("getCourseIdByIdx" + str(i)); return -1

  ################## get course ids by prefix##################

  def getCourseIdsByPrefix(self, prefix): 
    try:
      if prefix not in self.courseIdsByPrefix: self.msg("getCourseIdsByPrefix: prefix not found: " + prefix); return None
      return self.courseIdsByPrefix[prefix]
    except:
      self.err("getCourseIdsByPrefix issue"); return None

  ################## get course by index ##################

  def getCourseByIdx(self, i): 
    try:
      cid    = self.getCourseIdByIdx(i)
      result = self.coursesDict[cid]
      if self.verbose: msgStr = "getCourseByIdx %i: %s" % (i, str(result)); print(msgStr) 
      return result
      
    except: self.err("getCourseByIdx issue: " + str(i)); return -1

################## main ##################

if __name__ == "__main__":
  courses = Courses()
  courses.printCourseIds()

### end ###
