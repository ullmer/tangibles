# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import spectra
import pygame

from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesCsv        import *
from courseAssignments import *

portrait=False #mini display default-configs as portrait
if portrait: WIDTH, HEIGHT = 480, 1920
else:        WIDTH, HEIGHT = 1920, 480

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

################### coursesPg ################### 

class CoursesPgz(Courses):

  rows, cols =   9,   5
  dx,  dy1   = 207,  63 #dy1:   between blocks
  dy2, dy3   =   8,  17 #dy2/3: lines within/between blocks
  x0, y0     =  49,  28
  x1, y1     =  56,  37
  x2, x3     =   7,  42 #offsets from left edge of course block to left of course #, title/instructor
  y2, y3     =  -2,  26 #offsets from  top edge of course block to  top of           title,instructor

  actorCats    = ['cs', 'hcc', 'vc', 'foi']
  actorCatDict = None   #actor category dictionary; contemplating graceful paths to manage pi ram
  actor2id     = None
  #numRd       = None
  numRd        = 0

  backdropFn   = 'ak_apc_mm2_d03_1920'
  backdropA    = None

  divisionBackdrops = ['ak_apc_mm2_d03_1920_a', 'ak_apc_mm2_d03_1920_b', 
                       'ak_apc_mm2_d03_1920_c', 'ak_apc_mm2_d03_1920_d']
  divisionBackdropA = None

  rrectX, rrectY = 336, 92
  courseGroups   = None
  timeDotActors  = None     #time dots currently legacy of readings representation, though...
  timeDotImgFn   = 'time_circ01e'
  timeDotX       = 100
  timeDotY       = 900
  timeDotDX      = 80

  font1      = "o1" #need to add auto-retrieval from fonts/o1.url if o1.ttf not present
  fontSize   = 24
  cwhite     = "#ffffff"
  cblack     = "#000000"
  #actorBgFn  = 'courses_box_1c'

  #colorScaleColors = ['orange', 'purple']
  #colorScaleColors = ['yellow', 'white', 'cyan', 'chartreuse', 'mauve']
  colorScaleColors  = ['yellow', 'gold', 'white', 'cyan', 'chartreuse', 'violet']
  colorScale = None

  drawExtraAnnotatives  = True

  actorSelectedId       = None
  dotSelected           = False
  courseTextDrawOffset  = None
  connectingLineWidth   = 3
  olderPgz              = True # suppress line widths and fading for std=older pip pgz version

  ################## constructor, error ##################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()
    self.actor2id              = {}
    self.courseTextDrawOffset  = {}
    self.timeDotActors         = {}
    self.courseGroups          = {}

    try:    self.colorScale = spectra.scale(self.colorScaleColors)    //A
    except: print("problems with color scale; spectra probably not installed"); pass #if spectra installed, do the right thing

    #self.numRd    = self.size()
    rxc           = self.rows * self.cols
    if self.numRd > rxc: self.numRd = rxc

    self.buildUI()

  ################## error ##################

  def err(self, msg): print("CoursesPgz error:", msg); traceback.print_exc()
  def msg(self, msg): print("CoursesPgz msg:",   msg)

  #def checkPgzVersion(self): 
  #  print(dir(pgzero.builtins))
  #  return pgzero.__version__

  ################## get course group color ##################

  def getCourseGroupColor(self, courseGroupId, colorType): 
    if self.numCourseGroups is None: #unassigned; error, sigh
      self.err("getGroupColor: numCourseGroups unassigned!"); return '#aaa'; #gray

    if self.colorScale is None: return '#c99' #spectra not installed, return red

    ratio = float(courseGroupId) / float(self.numCourseGroups)
    #result = self.colorScale(ratio).rgb

    if colorType == 'hex': result = self.colorScale(ratio).hexcode
    else:                  r,g,b = self.colorScale(ratio).rgb; result = (r*255, g*255, b*255)
    return result

  ################## build UI ##################

  def buildUI(self): 
    row, col = 0, 0
    x, y     = self.x0, self.y0

    self.backdropA = Actor(self.backdropFn)

    #print("PGZ version: ", self.checkPgzVersion())

    if self.divisionBackdrops is not None:
      idx = 0; self.divisionBackdropA = []
      for divisionBackdrop in self.divisionBackdrops:
        a = Actor(divisionBackdrop) 
        self.divisionBackdropA.append(a)

    for i in range(self.numRd):
      a = Actor(self.actorBgFn, topleft=(x, y))
      y += self.dy1; row += 1; self.actor2id[a] = i

      if row >= self.rows: 
        row = 0; col += 1; y = self.y0; x += self.dx

  ################## calculate course position by id ##################

  def calcCoursePosById(self, courseId): 
    self.msg("calcCoursePosById: needs refactoring"); return
    try:
      actor  = self.actors[courseId]
      result = actor.pos
      return result
    except: self.err("calcCoursePosById on courseId " + str(courseId)); return None

  ################## draw ##################

  def draw(self, screen): 
    row, col = 0, 0
    x, y     = self.x0, self.y0

    if self.backdropA is not None: self.backdropA.draw()

    a = self.divisionBackdropA[1]; a.topleft=(500,50); a.draw()

    hccPrefixCourses = self.getCourseIdsByPrefix('HCC')
    self.msg("draw: hccPrefixCourses: " + str(hccPrefixCourses))

    x0, y0 = 500, 25
    for hccpc in hccPrefixCourses: self.drawCourse(screen, hccpc, x0, y0); y0 += self.y1
    
    for i in range(self.numRd):
      if i in self.courseTextDrawOffset: textDrawOffsetsSaved = True
      else:                               textDrawOffsetsSaved = False

      if textDrawOffsetsSaved:
        x2, y2 = self.courseTextDrawOffset[i]
      else:
        self.courseTextDrawOffset[i] = (x, y)
        x2, y2 = x, y

      self.drawCourse(screen, i, x2, y2)

      if not(textDrawOffsetsSaved): # we need to calculate them. Logic should be relocated
        y += self.dy; row += 1

        if row >= self.rows: 
          row = 0; col += 1; y = self.y0; x += self.dx

  ################## draw lines amongs courses in groups ##################

  def drawLinesAmongCoursesInGroups(self, screen): 
    for i in range(self.numCourseGroups):
      courseIds = self.courseGroups[i]
      lri = len(courseIds)
      if lri == 1: continue #nothing to do, onwards
      rgcolor = self.getCourseGroupColor(i, 'rgb')

      if lri >= 2:
        id0, id1 = courseIds[0], courseIds[1]
        self.drawLineBetweenCourses(screen, id0, id1, rgcolor, self.connectingLineWidth)
        if lri > 2:
          for j in range(2, lri):
            id0 = courseIds[j-1]
            id1 = courseIds[j]
            self.drawLineBetweenCourses(screen, id0, id1, rgcolor, self.connectingLineWidth)

  ################## on_mouse_down ##################

  def on_mouse_down(self, pos): 
    for i in range(self.numRd):
      actor = self.actors[i]
      if actor.collidepoint(pos): 
        print("Actor selected:", i)
        self.actorSelectedId = i
        return

  ################## on_mouse_move ##################

  def on_mouse_move(self, rel, buttons): 
    if self.actorSelectedId is not None:
      id     = self.actorSelectedId

      if not(self.dotSelected): actor  = self.actors[id]                           //A
      else:                     actor  = self.timeDotActors[id]

      x1, y1 = actor.pos
      dx, dy = rel
      x2, y2 = x1+dx, y1+dy

      if id in self.courseTextDrawOffset and not(self.dotSelected): 
        x3, y3 = self.courseTextDrawOffset[id]
        x4, y4 = x3+dx, y3+dy
        self.courseTextDrawOffset[id] = (x4, y4)

      actor.pos = (x2, y2)

  def on_mouse_up(self): 
     self.actorSelectedId = None
     self.dotSelected     = False

  ################## draw course ################## 
  
  def drawCourse(self, screen, courseId, x0, y0):
    course = self.getCourseById(courseId)
    if course is None: self.msg("drawCourse: no course found for id " + str(courseId)); return

    instr, cabbrev, subj, crse = course.getFields(['Instructor', 'abbrevTitle', 'Subj', 'Crse'])
    instr = instr.lower()
    courseIdFirst2 = crse[0:2]
    courseIdLast2  = crse[-2:]          
  
    f1, fs = self.font1, self.fontSize
    c1     = self.cwhite

    x2, x3, y2, y3 = self.x2, self.x3, self.y2, self.y3 # for compact ref below

    #x2, x3     =   4,  42 #offsets from left edge of course block to left of course #, title/instructor
    #y2, y3     =   6,  30 #offsets from  top edge of course block to  top of           title,instructor
  
    screen.draw.text(courseIdFirst2,   topleft  = (x0 + x2, y0 + y2), fontsize=fs, fontname=f1, color=c1, alpha=0.6) 
    screen.draw.text(courseIdLast2,    topleft  = (x0 + x2, y0 + y3), fontsize=fs, fontname=f1, color=c1, alpha=0.6) 
    screen.draw.text(cabbrev,          topleft  = (x0 + x3, y0 + y2), fontsize=fs, fontname=f1, color=c1, alpha=0.6)
    screen.draw.text(instr,            topleft  = (x0 + x3, y0 + y3), fontsize=fs, fontname=f1, color=c1, alpha=0.5)

################## main ################## 

cpgz = CoursesPgz()
#cpgz.printCourseIds()

#if __name__ == "__main__":

def draw(): screen.clear(); cpgz.draw(screen)
def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
