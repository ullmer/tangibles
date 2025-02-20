# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2025-02-20

import yaml, traceback

################## Course class ##################

class Project: #not catching any errors; caveat emptor

  verbose         = False
  quiet           = True  #suppress several warnings
  studentInitials, projName = None, None
  yamlFn          = 'projects.yaml'

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

  def msg(self, msg): print("Project msg:",   msg)
  def err(self, msg): print("Project error:", msg); traceback.print_exc()

  def print(self): 
    str = "Project %s [Students: %s]" % (self.projName, self.studentInitials)
    print(str)

  ################## loadYaml ##################

  def __init__(self, **kwargs):

### end ###
