# Evolving hccCoursesYaml to course-related CSV variation
# Brygg Ullmer, Clemson University
# Original written 2025-02-20

import yaml, traceback

################## project base class ##################

class Project: 

  verbose         = False
  peopleAbbrev, projName, projHandle = None, None, None

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

  def msg(self, msg): print("Project msg:",   msg)
  def err(self, msg): print("Project error:", msg); traceback.print_exc()

  def print(self): 
    str = "Project %s [Students: %s]" % (self.projName, self.studentInitials)
    print(str)

################## project base class ##################
class Projects: 
  yamlFn    = 'projects.yaml'
  yamlD     = None
  projects  = None
  
################## loadYaml ##################

  def loadYaml(self): 
    f  = open(self.yamlFn, 'rt')
    yd = self.yamlD = yaml.safe_load(f)
    f.close()
   
    self.projects  = {}

    if 'projects' not in yd:         self.msg("loadYaml: projects not found"); return
    yp = yd['projects']
    for projId in yp:
      proj = projects[projId]
      if 'peopleAbbrev' not in proj: continue # silently ignore initially
      pa = proj['peopleAbbrev']

      ph, pn = None, None
      if 'projName'   in proj: pn = proj['projName']
      if 'projHandle' in proj: ph = proj['projHandle']
      
      p = Project(peopleAbbrev=pa, projName=pn, projHandle=ph)
      self.projects[projId] = p

  def print(self): 
    for projId in self.projects: 
      proj = self.projects[projId]
      proj.print()

### end ###

