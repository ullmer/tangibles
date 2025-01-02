# Example parsing class course list
# Brygg Ullmer, Clemson University
# Begun 2024-09-05

import os, traceback
import spectra
import pygame

from pgzero.builtins   import Actor, animate, keyboard, keys
from coursesCats       import *

portrait=False #mini display default-configs as portrait
if portrait: WIDTH, HEIGHT = 480, 1920
else:        WIDTH, HEIGHT = 1920, 480

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

################### coursesPgzBase ################### 

#class CoursesPgzBase(Courses):
class CoursesPgzBase(CoursesCats):

  rows, cols =   9,   5
  dx,  dy1   = 205,  67 #dy1:   between blocks
  dy2, dy3   =   8,  17 #dy2/3: lines within/between blocks
  x0,  y0    =  38,  28 # column bounding boxes
  x0b, y0b   =  53,  30 # placements within columns of content
  x1, y1     =  55,  37
  x2, x3, x4 =   9,  44,  7 #offsets from left edge of course block to left of course #, title/instructor, subj
  y2, y3, y4 =  -2,  26, 55 #offsets from  top edge of course block to  top of           title,instructor

  barDy1, barDy2 = 7, 13

  actorCats     = ['cs', 'hcc', 'vc', 'foi']
  actorCatDict  = None   #actor category dictionary; contemplating graceful paths to manage pi ram
  actor2id      = None
  #numRd        = None
  numRd         = 0

  backdropFn   = 'ak_apc_mm2_d03_1920'
  backdropA    = None

  divisionBackdrops = ['ak_apc_mm2_d03_1920_a', 'ak_apc_mm2_d03_1920_b', 
                       'ak_apc_mm2_d03_1920_c', 'ak_apc_mm2_d03_1920_d']
  divisionBackdropA = None
  drawSampleContent = True

  rrectX, rrectY = 336, 92
  crectX, crectY = 180, 4
  courseGroups   = None

  font1      = "o1" #need to add auto-retrieval from fonts/o1.url if o1.ttf not present
  fontSize1  = 24
  fontSize2  = 17.5
  cwhite     = "#ffffff"
  cblack     = "#000000"
  #divColors  = ['#EFDBB2', '#B94700', '#546223', '#005EB8']
  #divColors  = ['#5f5747', '#A43800', '#2a3111', '#005EB8']
  divColors  = ['#474135', '#B94700', '#323a15', '#005EB8']

  #colorScaleColors = ['orange', 'purple']
  #colorScaleColors = ['yellow', 'white', 'cyan', 'chartreuse', 'mauve']
  colorScaleColors  = ['yellow', 'gold', 'white', 'cyan', 'chartreuse', 'violet']
  colorScale = None

  actorSelectedId       = None
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

  ################## draw ##################

  def draw(self, screen): 
    row, col = 0, 0
    x, y     = self.x0, self.y0

    if self.backdropA is not None: self.backdropA.draw()

    #if self.drawSampleContent: self.drawSamples1(screen)
    if self.drawSampleContent:  self.drawSamples2(screen)

  ################## draw samples #2 ##################

  def drawSamples2(self, screen): 

    colorIndices = [3,1,2,0]

    bds = [] #backdrops/backgrounds of individual courses, across several colors
    for i in colorIndices: bds.append(self.divisionBackdropA[i])

    dcs = [] # toward colorbars. refactor next line & above
    for i in colorIndices: dcs.append(self.divColors[i]) 

    x0     = self.x0b  #refactor names
    cats   = self.getCats()
    colIdx = 0

    for cat in cats:
      y0 = self.y0b
      courses = self.getCoursesInCat(cat)
      catDivs = []

      idx = 0
      for courseID in courses:
        div    = self.mapCourseToDivisions(courseID)
        if div is None: self.msg("drawSamples2: ignoring null div"); continue

        divLow = div.lower()
        if divLow in self.actorCats: divIdx = self.actorCats.index(divLow)
        else:                        self.msg("drawSamples2: ignoring div issue: " + str(divLow)); continue
        backdrop = bds[divIdx]; barColor=dcs[divIdx]

        if idx < 3: 
          backdrop.topleft=(x0, y0); backdrop.draw()
          self.drawCourse(screen, courseID, x0, y0, barColor)
          y0 += self.dy1
        else: 
          self.drawCourseBar(screen, courseID, x0, y0, barColor); y0 += self.barDy1

        idx += 1

      x0 += self.dx
        
  ################## draw samples #1 ##################

  def drawSamples1(self, screen): 
    a = self.divisionBackdropA[1]
    b = self.divisionBackdropA[2]
    c = self.divisionBackdropA[0]

    hccPrefixCourses = self.getCourseIdsByPrefix('HCC')
    dpaPrefixCourses = self.getCourseIdsByPrefix('DPA')
    csPrefixCourses = self.getCourseIdsByPrefix('CPSC')

    c1, c2, c3, c4 = self.divColors

    x0, y0 = 1283, 30; idx = 0
    for hccpc in hccPrefixCourses: 
      a.topleft=(x0, y0); a.draw()
      self.drawCourse(screen, hccpc, x0, y0, c2); y0 += self.dy1
      #self.drawCourseBar(screen, hccpc, x0, y0, c2); idx += 1
      #if idx % 4 == 0: y0 += 13
      #else:            y0 += 7

    x0 += self.dx; y0 = 30; idx = 0
    for dpapc in dpaPrefixCourses: 
      #b.topleft=(x0, y0); b.draw()
      #self.drawCourse(screen, dpapc, x0, y0, c3); y0 += self.dy1
      self.drawCourseBar(screen, dpapc, x0, y0, c3); idx += 1
      if idx % 4 == 0: y0 += 13
      else:            y0 += 7

    x0 -= self.dx*2; y0 = 30; idx = 0
    for cspc in csPrefixCourses: 
      #c.topleft=(x0, y0); c.draw()
      self.drawCourseBar(screen, cspc, x0, y0, c1); idx += 1
      if idx % 4 == 0: y0 += 13
      else:            y0 += 7

    #return
    # 
    #for i in range(self.numRd):
    #  if i in self.courseTextDrawOffset: textDrawOffsetsSaved = True
    #  else:                              textDrawOffsetsSaved = False

    #  if textDrawOffsetsSaved:
    #    x2, y2 = self.courseTextDrawOffset[i]
    #  else:
    #    self.courseTextDrawOffset[i] = (x, y)
    #    x2, y2 = x, y

    #  self.drawCourse(screen, i, x2, y2)

    #  if not(textDrawOffsetsSaved): # we need to calculate them. Logic should be relocated
    #    y += self.dy; row += 1

    #    if row >= self.rows: 
    #      row = 0; col += 1; y = self.y0; x += self.dx

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
  
  def drawCourseBar(self, screen, courseId, x0, y0, color):
    rrect  = pygame.Rect(x0, y0, self.crectX, self.crectY)
    screen.draw.rect(rrect, color, width=0)

    #if self.olderPgz: screen.draw.rect(rrect, rcolor)
    #else:             screen.draw.rect(rrect, rcolor, width=2)

  ################## draw course ################## 
  
  def drawCourse(self, screen, courseId, x0, y0, color):
    course = self.getCourseById(courseId)
    x0 += 16

    if course is None: self.msg("drawCourse: no course found for id " + str(courseId)); return

    if course.hasField('abbrevTitle') is False: self.msg("ignoring " + courseId); return

    instr, cabbrev, subj, crse = course.getFields(['InstructorTrunc', 'abbrevTitle', 'Subj', 'Crse'])
    instr = instr.lower()
    courseIdFirst = crse[0:2]

    if crse[-1].isdigit(): courseIdLast = crse[-2:]
    else:                  courseIdLast = crse[-3:]
  
    f1, fs1, fs2 = self.font1, self.fontSize1, self.fontSize2
    c1           = self.cwhite

    x2, x3, x4, y2, y3, y4 = self.x2, self.x3, self.x4, self.y2, self.y3, self.y4 # for compact ref below

    #x2, x3     =   4,  42 #offsets from left edge of course block to left of course #, title/instructor
    #y2, y3     =   6,  30 #offsets from  top edge of course block to  top of           title,instructor
  
    screen.draw.text(courseIdFirst,   topleft = (x0 + x2, y0 + y2), fontsize=fs1, fontname=f1, color=c1, alpha=0.6) 
    screen.draw.text(courseIdLast,    topleft = (x0 + x2, y0 + y3), fontsize=fs1, fontname=f1, color=c1, alpha=0.6) 
    screen.draw.text(cabbrev,         topleft = (x0 + x3, y0 + y2), fontsize=fs1, fontname=f1, color=c1, alpha=0.6)
    screen.draw.text(instr,           topleft = (x0 + x3, y0 + y3), fontsize=fs1, fontname=f1, color=c1, alpha=0.5)
    screen.draw.text(subj,         bottomleft = (x0 + x4, y0 + y4), fontsize=fs2, fontname=f1, color=c1, alpha=0.6, angle=90)

################## main ################## 


#if __name__ == "__main__":
#cpgzb = CoursesPgzBase()
#cpgz.printCourseIds()
#print(cpgz.courseIdsByPrefix)

#def draw(): screen.clear(); cpgzb.draw(screen)
#def on_mouse_down(pos):     pass #cpgz.on_mouse_down(pos)

### end ###
