# Class representing importing + engaging one representations of course assignments
# Brygg Ullmer, Clemson University
# Begun 2024-12-21

import csv, sys, traceback
from socDb import * #school of computing database

class courseAssignments:
  csvFn       = 'S25.csv'
  csvD        = None
  tableFields = None
  tableRows   = None
  socDbInst   = None
  mapNameR2C  = None
  mapNameC2D  = None
  mapNameD2C  = None
  mapCourse2Div   = None
  mapDiv2Courses  = None
  mapCourse2Title = None

  faculty2div = None
  div2faculty = None
  instructors = None

  ############# msg, err #############
  
  def msg(self, msgStr): print("courseAssignments msg:", msgStr)
  def err(self, msgStr): print("courseAssignments err:", msgStr)

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.loadCsv()
    self.socDbInst = socDb()
    self.mapInstructorsC2S()
    self.mapCourseInstructorsToDivisions()
    self.mapCoursesToDivisions()
 
  ############# loadCsv #############

  def loadCsv(self):
    if self.csvFn is None: self.err("loadCsv: csvFn is empty!"); sys.exit(-1)
    firstRow = True

    try:
      csvF = open(self.csvFn, 'rt')
      csvR = csv.reader(csvF, delimiter=',', quotechar='"')
      for row in csvR:
        if firstRow: self.tableFields = row; self.tableRows = []; firstRow=False #header
        else:        self.tableRows.append(row)
    except:
      self.err("loadCsv import exception")
      traceback.print_exc()

  ############# extract field values #############

  def extractFieldVals(self, fieldName):
    if fieldName not in self.tableFields: self.err("extractFieldVals: specified field name not found"); return

    try:
      fieldId = self.tableFields.index(fieldName)
      result = []
      for row in self.tableRows:
        val = row[fieldId]
        result.append(val)

      return result
    except:
      self.err("extractFieldVals exception")
      traceback.print_exc(); return False

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

    except:
      self.err("mapCoursesToDivisions exception")
      traceback.print_exc(); return False

############# main #############

if __name__ == "__main__":
  ca = courseAssignments()
  #print(ca.tableFields) 
  subjs = ca.extractFieldValsUnique('Subj')
  print(ca.div2faculty['HCC'])
  print(ca.mapDiv2Courses['HCC'])
  for c in ca.mapDiv2Courses['HCC']: print(ca.mapCourse2Title[c])

  for div in ca.mapDiv2Courses:
    ndiv = len(ca.mapDiv2Courses[div])
    print(div, ndiv)

### end ###

