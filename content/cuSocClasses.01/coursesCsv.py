# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2024-09-05
# Evolution begun  2024-12-25

import csv, traceback

################## Course class ##################

class Course: #not catching any errors; caveat emptor

  fields          = ['author', 'year', 'abbrevTitle', 'title', 'presenter', 'presentedDate']
  readingGroupNum = None
  fieldsDict      = None

  ################## constructor, error ##################

  def __init__(self): 
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.fieldsDict = {}

  def err(self, msg): print("Course error:", msg); traceback.print_exc()

  ################## set fields from yaml ##################

  def setFieldsFromYaml(self, yd):
    try: 
      for field in self.fields: self.fieldsDict[field] = yd[field]
    except: self.err('setFieldsFromYaml')
    
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

  def printCourseAbbrev(self):    
    try:    print(self.fieldsDict['abbrevTitle'])
    except: self.err('printCourseAbbrev')

  def print(self): print(self.fieldsDict)   

################## Courses class ##################

class Courses: #not catching any errors; caveat emptor
  fn          = 'S25.csv'  #filename
  csvD        = None       #CSV data
  coursesList = None
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
    self.coursesList = []
    try:
      f       = open(self.fn, 'rt')
      self.yd = yaml.safe_load(f)
      self.yc = self.yd['class'] 
      idx     = 0

      for classDate in self.yc:
        classPeriod = self.yc[classDate]
        self.numCourseGroups += 1 
        for reading in classPeriod:
          reading['presentedDate'] = classDate

          r = Course()
          r.setFieldsFromYaml(reading)
          r.readingGroupNum = idx
          self.readingList.append(r)

        idx += 1 # by class period, not reading #

    except: self.err("loadYaml")

  ################## print reading abbreviations ##################

  def printCourseAbbrevs(self): 
    try:
      for r in self.readingList: r.printCourseAbbrev()
    except: self.err("printCourseAbbrevs")

  ################## get reading index ##################

  def getCourse(self, i): 
    try:
      if i < 0 or i > len(self.readingList): self.err("getCourse index out of bounds: " + i); return
      return self.readingList[i]
      
    except: self.err("getCourse: " + i); return

################## main ##################

if __name__ == "__main__":
  courses = Courses()
  courses.loadYaml()
  courses.printCourseAbbrevs()

### end ###
