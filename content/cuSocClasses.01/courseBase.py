# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2024-09-05
# Evolution begun  2024-12-25

import csv, traceback

################## Course class ##################

class Course: #not catching any errors; caveat emptor

  fieldsDict      = None
  verbose         = False
  quiet           = True  #suppress several warnings
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
      cid = self.getCourseId()
      if self.verbose: 
        if cid is None: self.msg("setFields: " + str(fieldNames) + str(fieldVals))
        else:           self.msg("setFields: " + cid + str(fieldNames) + str(fieldVals))

      for fieldName, fieldVal in zip(fieldNames, fieldVals):
        self.setField(fieldName, fieldVal)

      if self.verbose: self.msg("setFields post-assignment: " + str(self.fieldsDict))
    except: self.err('setFields issue')
    
  ################## set field ##################

  def setField(self, field, val):  
    try:    self.fieldsDict[field] = val
    except: self.err('setField issue' + field + val)

  ################## has field(s) ##################

  def hasField(self, field):       
    try:    
      if field in self.fieldsDict: return True
      return False
    except: self.err('hasField' + field)

  def hasFields(self, fields):
    try:    
      for field in fields: 
        if not self.hasField(field): return False
      return True
    except: self.err('hasFields' + field)

  ################## get field ##################

  def getField(self, field):       
    try:    return self.fieldsDict[field]
    except: self.err('getField' + field)

  ################## get fields ##################

  def getFields(self, fields):       
    result = []

    if self.fieldsDict is None:      self.msg("getFields issue: fields dictionary not instantiated!"); return None
    if not isinstance(fields, list): self.msg("getFields issue: argument fields is not a list!");      return None

    try:    
      for field in fields: result.append(self.fieldsDict[field])
    except: 
      self.err('getFields ' + field)
      #self.msg('known fields: ' + str(list(self.fieldsDict.keys())))
      return None

    return result

  ################## print ##################

  def getCourseId(self):
    if self.fieldsDict is None:              self.msg("getCourseId issue: fields dictionary not instantiated!"); return None
    if not self.hasFields(['Subj', 'Crse']): 
      if self.verbose:     self.msg("getCourseId issue: does not have both Subj and Crse!")
      elif not self.quiet: print("!", end='')
      #self.msg(str(self.fieldsDict))
      return None

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
