# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2024-09-05
# Evolution begun  2024-12-25

import csv, traceback

################## Course class ##################

class Course: #not catching any errors; caveat emptor

  fieldsDict      = None
  verbose         = False

  ################## constructor, error ##################

  def __init__(self, **kwargs):
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
    except: self.err('getFields' + field)

    return result

  ################## print ##################

  def getCourseId(self):
    try:
      subj, crse = self.getFields(['Subj', 'Crse'])
      result = subj + crse
      return result
    except: self.err("getCourseId issue")

  def printCourseId(self): cid = self.getCourseId(); print(cid)

  ################## print ##################

  def printCourseAbbrev(self):    
    try:    print(self.fieldsDict['abbrevTitle'])
    except: self.err('printCourseAbbrev')

  def print(self): print(self.fieldsDict)   

################## Courses class ##################

class Courses: #not catching any errors; caveat emptor
  fnMain           = 'S25.csv'        #filename
  fnAbbrev         = 'S25abbrev.csv'  #filename
  csvDMain         = None             #CSV data
  csvDAbbrev       = None             
  csvHeaderFieldsM = None
  csvHeaderFieldsA = None
  coursesDict      = None
  numCourseGroups  = 0
  verbose          = False

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
    self.coursesDict = {}
    try:
      f        = open(self.fnMain, 'rt')  
      rdr      = csv.reader(f, delimiter=',', quotechar='"')
      firstRow = True

      for row in rdr:   ### Process main file
        if firstRow: self.processCsvHeaderMain(row); firstRow = False; continue
        c = Course()
        c.setFields(self.csvHeaderFields, row)

        crse = c.getField('Crse')
        if crse.find('4+6') > -1: crse2 = 'x' + crse[3:]; c.setField('Crse', crse2)
        if c.getField('Crse').find('4+6') > -1: c.setField
        courseId = c.getCourseId()
        self.coursesDict[courseId] = c

      f.close()

      f        = open(self.fnAbbrev, 'rt') # Read abbrev file next
      rdr      = csv.reader(f, delimiter=',', quotechar='"')
      firstRow = True

      for row in rdr:   ### Process abbreviations file
        if firstRow: firstRow = False; continue
   
        try:
          if len(row) == 3: subject, course, abbrev = row
          else: self.msg("loadCsv problem with abbrev file re input: " + str(row)); continue

          courseID = subject + course
          c = self.getCourseById(courseID)
          if c is None: self.msg("loadCsv: problem in assigning abbrev to " + courseId)
          else: c.setField('abbrevTitle', abbrev)
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

  ################## get course by idx ##################

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
