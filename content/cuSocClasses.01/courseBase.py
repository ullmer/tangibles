# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2024-09-05
# Evolution begun  2024-12-25

import csv, traceback

################## Course class ##################

class Course: #not catching any errors; caveat emptor

  fieldsDict      = None
  verbose         = False
  cats            = None #categories

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

  ################## has field ##################

  def hasField(self, field):       
    try:    
      if field in self.fieldsDict: return True
      return False
    except: self.err('hasField' + field)

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

### end ###
