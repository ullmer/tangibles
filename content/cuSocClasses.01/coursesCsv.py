# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2024-09-05
# Evolution begun  2024-12-25

import csv, traceback

################## Course class ##################

class Course: #not catching any errors; caveat emptor

  fields          = None
  readingGroupNum = None
  fieldsDict      = None

  ################## constructor, error ##################

  def __init__(self): 
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.fieldsDict = {}

  def msg(self, msg): print("Course msg:",   msg)
  def err(self, msg): print("Course error:", msg); traceback.print_exc()

  ################## set fields ##################

  def setFields(self, fieldNames, fieldVals):
    try: 
      for fieldName, fieldVal in zip(fieldNames, fieldVals):
        self.setField(fieldName, fieldVal)
    except: self.err('setFields')
    
  ################## set field ##################

  def setField(self, field, val):  
    try:    self.fieldsDict[field] = val
    except: self.err('setField' + field + val)

  ################## get field ##################

  def getField(self, field):       
    try:    return self.fieldsDict[field]
    except: self.err('getField' + field)

  ################## get field ##################

  def getFields(self, fields):       
    result = []

    try:    
      for field in fields: result.append(self.fieldsDict[field])
    except: self.err('getField' + field)

    return result

  ################## print ##################

  def getCourseId(self):
    try:
      subj, crse = self.getFields(['Subj', 'Crse'])
      result = subj + crse
      return result
    except: self.err("getCourseId issue")

  ################## print ##################

  def printCourseAbbrev(self):    
    try:    print(self.fieldsDict['abbrevTitle'])
    except: self.err('printCourseAbbrev')

  def print(self): print(self.fieldsDict)   

################## Courses class ##################

class Courses: #not catching any errors; caveat emptor
  fn              = 'S25.csv'  #filename
  csvD            = None       #CSV data
  csvHeaderFields = None
  coursesDict     = None
  numCourseGroups = 0

  ################## constructor, err ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.loadCsv()
  
  def err(self, msg): print("Courses error:", msg); traceback.print_exc()

  def size(self): 
    if self.readingList is not None: return len(self.readingList)

  ################## load YAML from file ##################

  def loadCsv(self): 
    self.coursesDict = {}
    try:
      f   = open(self.fn, 'rt')
      rdr = csv.reader(f, delimiter=',', quotechar='"')

      firstRow = True

      for row in rdr:
        if firstRow: self.processCsvHeader(); firstRow = False
        else:       
          c = Course()
          c.setFields(self.csvHeaderFields, row)
          courseId = c.getCourseId()
          self.coursesDict[courseId] = c

    except: self.err("loadCsv issue")

  ################## process CSV header ##################

  def processCsvHeader(self, row): 
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
        c = self.getCourseByIdx(i); c.printCourseAbbrev()
    except: self.err("printCourseIds issue")

  ################## get number of courses ##################

  def getNumCourses(self): 
    try:
      cidList = list(self.coursesDict.keys())
      return len(cidList)
    except: self.err("getNumCourses issue:")

  ################## get course by idx ##################

  def getCourseByIdx(self, i): 
    try:
      cidList = list(self.coursesDict.keys())
      if i < 0 or i > len(cidList): self.err("getCourse index out of bounds: " + i); return
      return cidList[i]
      
    except: self.err("getCourseByIdx issue: " + i); return

################## main ##################

if __name__ == "__main__":
  courses = Courses()
  courses.printCourseIds()

### end ###
