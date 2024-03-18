# Poster++ tangibles-supported browser code
# Brygg Ullmer, Clemson University
# Begun 2024-03-17

import moveWinHome #hack to move window to 0,0 on windows, avoiding redraw error

WIDTH  = 2160
HEIGHT = 3660

import time as pytime #since pgzero maps pygame time to "time"
import pygame
import yaml
import traceback

from posterMidi        import *
from enoMidiController import *

class posterBrowser:
  topBlockFn   = 'full_res/top_block01'
  upperHlBoxFn = 'full_res/upper_highlight_box'
  brHlBoxFn    = 'bottom_rightv08g_cursor'
  brBlockFn    = 'bottom_rightv08g'
  ypfn         = 'posters-iui24.yaml'
  ygfn         = 'geos.yaml'
  ypd          = None
  ygd          = None

  topBlockPos          = (0, 0)
  upperHlBoxBasePos    = (13,218)
  upperHlBoxRelPos     = (0, 0)
  upperHlBoxRelMaxPos  = (7, 7)
  upperHlBoxDiffPos    = (266, 183)
  lastHighlightedCoord = None

  brHlBoxDiffPos       = (118, 118)
  brHlBoxBasePos       = (1212,455)
  #brHlBoxBasePos      = (98,455)
  #brHlBoxBasePos      = (1209, 2533)

  posterNormPos       = (0,    1210)
  posterNormDim       = (2160, 1215)

  metaBlockNormPos    = (   0,   10)
  #metaBlockNormPos   = (   0, 2508)
  titlebarWidthHeight = (2160,   70)
  titlebarColor       = (60, 60, 60)

  brBlockNormPos      = (1214, 100) #for debugging on laptop
  #brBlockNormPos     = (1214, 2538)
  brBlockNormDim      = ( 946, 1302)
  brBlockMaximize     = False

  cursorAnimDur       = .5
  posterAnimDur       = .75
  #posterAnimDur      = 3.
  animTween           = 'accel_decel'
  requestMaximize     = True

  useMidiController   = True
  emc                 = None #enodia midi  controller handle
  pmc                 = None #enodia poster midi controller handle

  numPosters           = 34
  posterFnPrefix       = 'posters.0315a/screen_res/iui24_'
  posterActors         = None
  lastPoster           = None
  activePoster         = 1
  cyclePosters         = True #automatically cycle between posters
  #cyclePosterFrequency = 10.  #how frequently to make the cycling
  cyclePosterFrequency = 3.  #how frequently to make the cycling

  autoAdvanceSlides          = True
  cyclePosterAutolaunchDelay = 60. #after how many seconds should autolaunch begin
  lastPosterAnimTimeBegun    = None

  topBlockA    = None #pgzero actors
  upperHlBoxA  = None
  brBlockA     = None 
  brHlBoxA     = None
  brBlockMaxA  = None # maximized version of bottom-right interaction block

  firstDraw    = True 

  arrayDim = [8, 8]

  actors   = None
  scr      = None
  verbose  = True

  ######################## constructor ######################## 

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.constructActors()
    self.loadYaml()

    if self.useMidiController: self.launchMidiController()

  ######################## load yaml ######################## 

  def loadYaml(self): 
    ypf = open(self.ypfn, 'rt') #poster metainfo
    ygf = open(self.ygfn, 'rt') #geographical metainfo
    
    self.ypd = yaml.safe_load(ypf)
    self.ygd = yaml.safe_load(ygf)

  ###################### get poster metainfo ######################

  def getPosterMetainfo(self, posterId): 
    try:
      p = self.ypd['posters'][posterId]
      return p
    except:
      print("posterBrowser getPosterMetainfo issue for poster", posterId)
      traceback.print_exc()
      return None

  ###################### get poster title ######################

  def getPosterField(self, posterId, whichField): 
    try:
      posterD = self.getPosterMetainfo(posterId)
      val     = posterD[whichField]
      return val
    except:
      print("posterBrowser getPosterField issue for poster + field ", posterId, whichField)
      traceback.print_exc()
      return None

  ######################## poll ######################## 

  def poll(self): 
    if self.emc is not None: self.emc.pollMidi()
    else:                    print("posterBrowser poll: no midi binding present")

  ######################## launchMidiController ######################## 

  def launchMidiController(self): 
    if self.verbose: print("launchMidiController called")
    self.emc = enoMidiController('nov_launchpad_x') #'nov_launchpad_mk2'
    self.emc.clearLights()

    self.pmc = posterMidiController(emc=self.emc, useDefaultCb=False)
    self.emc.registerExternalCB(self.midiButtonCB)

    if self.verbose: print("launchMidiController completed")

  ######################## button callback ########################

  def midiButtonCB(self, emc, control, arg):
    if arg==0: return #key release
    x, y    = emc.addr2coord(control)
    if y == 13: y=0 # hack around bug

    #if self.lastHighlightedCoord is not None and y>0: #repeat buttons allowed for controllers
    if self.lastHighlightedCoord is not None and x>=0: #repeat buttons allowed for controllers
      lx, ly = self.lastHighlightedCoord
      if x==lx and y==ly: print("midiButtonCB: ignoring"); return
      self.pmc.normalLightButton(lx,ly)
      self.pmc.highlightDict[lx][ly] = False

    #if self.verbose: print("pb2 mbcb XY:", x, y, arg)
    rmaxX, rmaxY = self.upperHlBoxRelMaxPos 

    if 0<=x<rmaxX and 0<y<rmaxY:
      self.shiftCursorAbs(x, y-1)

    self.pmc.highlightDict[x][y] = True
    self.pmc.highlightButton(x,y)
    self.lastHighlightedCoord = (x,y)

    if y==0: 
      # couldn't get Conda to install Python 3.10 on Win device, so reverting to if/elif
      #match x: # https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/ 
      if   x==0: self.shiftCursorRel( 0, -1); print("up")
      elif x==1: self.shiftCursorRel( 0,  1); print("down")
      elif x==2: self.shiftCursorRel(-1,  0); print("left")
      elif x==3: self.shiftCursorRel( 1,  0); print("right")

  ######################## calcSelectedPoster ######################## 

  def calcSelectedPoster(self): 
    rx, ry = self.upperHlBoxRelPos
    mx, my = self.upperHlBoxRelMaxPos
    result = rx + ry * mx + 1
    if result < 1:               result = 1
    if result > self.numPosters: result = self.numPosters
    return result

  ######################## get poster actor ######################## 

  def getPosterActor(self, whichPoster):
    if self.posterActors is None:        self.posterActors = {}
    if whichPoster in self.posterActors: return self.posterActors[whichPoster]

    afn = '%s%02i' % (self.posterFnPrefix, whichPoster)

    a   = Actor(afn, topleft=self.posterNormPos)
    self.posterActors[whichPoster] = a
    return a

  ######################## constructActors ######################## 

  def constructActors(self):
    self.topBlockA   = Actor(self.topBlockFn,   topleft = self.topBlockPos)
    self.upperHlBoxA = Actor(self.upperHlBoxFn, topleft = self.upperHlBoxBasePos)

    self.brBlockA     = Actor(self.brBlockFn,    topleft = self.brBlockNormPos)
    self.brHlBoxA     = Actor(self.brHlBoxFn,    topleft = self.brHlBoxBasePos)
    #self.brBlockMaxA  = Actor(self.brBlockMaxFn, topleft = self.brBlockNormPos)

    self.posterActors = {}

    self.actors = [self.topBlockA, self.upperHlBoxA, self.brBlockA, self.brHlBoxA]

  ######################## remove titlebar######################## 

  def maximize(self):
    self.scr = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.toggle_fullscreen()
    self.firstDraw = False
     
  ######################## draw ######################## 

  def draw(self):
    if self.firstDraw and self.requestMaximize: self.maximize()

    if self.brBlockMaximize is False: #normal case

      if self.lastPosterAnimatingOut(): 
        pla = self.getPosterActor(self.lastPoster)
        pla.draw()

      pa = self.getPosterActor(self.activePoster)
      pa.draw()

      for actor in self.actors: actor.draw()
      self.drawPosterMetainfo()

    else: pass #br block is maximized

  ######################## draw poster metainformation ###############

  def drawPosterMetainfo(self): 
    basepos = self.metaBlockNormPos
    #may hardcode details here that should migrate either to class def or yaml

    tw, th   = self.titlebarWidthHeight
    tc       = self.titlebarColor
    tx1, ty1 = basepos
    tx2, ty2 = tx1+tw, ty1+th
    tr       = Rect((tx1, ty1), (tx2, ty2))

    screen.draw.filled_rect(tr, tc)

  ###################### shift cursor relative ######################

  def autoAdvancePosters(self):
    self.shiftCursorRel(1,0)

  ###################### animate last poster out ######################

  def animLastPosterOut(self, dx=None, dy=None):  
    if dx is None or dy is None: return #nothing to do
    if self.lastPoster  is None: return #again, nothing to do

    self.lastPosterAnimTimeBegun = pytime.time()

    fpx, fpy = self.posterNormPos #"full position"
    fpw, fph = self.posterNormDim #poster width, height
    destX    = fpx - fpw * dx 
    destY    = fpy - fph * dy 

    pa = self.getPosterActor(self.lastPoster)
    pa.topleft = fpx, fpy
    animate(pa, topleft=(destX, destY), duration=self.posterAnimDur, tween=self.animTween)

  ###################### animate active poster in ######################

  def animActivePosterIn(self, dx=None, dy=None):  
    if dx is None or dy is None: return #nothing to do
    if self.activePoster is None: return #again, nothing to do

    fpx, fpy = self.posterNormPos #"full position"
    fpw, fph = self.posterNormDim #poster width, height
    beginX    = fpx + fpw * dx
    beginY    = fpy + fph * dy

    pa = self.getPosterActor(self.activePoster)
    pa.topleft = (beginX, beginY)
    animate(pa, topleft=(fpx, fpy), duration=self.posterAnimDur, tween=self.animTween)

  ###################### is last poster still animating out ######################
 
  def lastPosterAnimatingOut(self): 
    if self.lastPosterAnimTimeBegun is None: return False #not animating

    timeBegun   = self.lastPosterAnimTimeBegun 
    currentTime = pytime.time()
    dt = currentTime - timeBegun
    if dt < self.posterAnimDur: return True
    return False

  ###################### display poster ######################

  def displayPoster(self, dx=None, dy=None): 
    selPosterNum = self.calcSelectedPoster() 
    print("selected poster number:", selPosterNum)
    self.lastPoster   = self.activePoster
    self.activePoster = selPosterNum

    self.animLastPosterOut( dx, dy)
    self.animActivePosterIn(dx, dy)

  ###################### shift cursor relative ######################

  def shiftCursorRel(self, dx, dy): 
    rx, ry = self.upperHlBoxRelPos
    relmax = self.upperHlBoxRelMaxPos 

    if   dy + ry < 0:         ry = relmax[1]
    elif dy + ry > relmax[1]: ry = 0
    else:                     ry += dy

    if   dx + rx < 0:         rx = relmax[0]; ry -= 1
    elif dx + rx > relmax[0]: rx = 0; ry += 1
    else:                     rx += dx

    if ry < 0: rx, ry = 1, 4

    self.upperHlBoxRelPos = (rx, ry)

    x1 = self.upperHlBoxBasePos[0] + rx * self.upperHlBoxDiffPos[0]
    y1 = self.upperHlBoxBasePos[1] + ry * self.upperHlBoxDiffPos[1]

    animate(self.upperHlBoxA, topleft=(x1,y1), duration=self.cursorAnimDur, tween=self.animTween)

    x2 = self.brHlBoxBasePos[0] + rx * self.brHlBoxDiffPos[0]
    y2 = self.brHlBoxBasePos[1] + ry * self.brHlBoxDiffPos[1]

    animate(self.brHlBoxA, topleft=(x2,y2), duration=self.cursorAnimDur, tween=self.animTween)

    if self.lastHighlightedCoord is not None:
      lx, ly = self.lastHighlightedCoord
      self.pmc.normalLightButton(lx,ly)
      self.pmc.highlightDict[lx][ly] = False
      dx, dy = lx-rx, ly-(ry+1)
    else: dx, dy = None, None

    self.lastHighlightedCoord=(rx, ry+1)
    self.pmc.highlightButton(  rx, ry+1)
    self.pmc.highlightDict[rx][ry] = True

    self.displayPoster(dx, dy)

  ###################### shift cursor absolute ######################

  def shiftCursorAbs(self, rx, ry): 

    self.upperHlBoxRelPos = (rx, ry)

    x1 = self.upperHlBoxBasePos[0] + rx * self.upperHlBoxDiffPos[0]
    y1 = self.upperHlBoxBasePos[1] + ry * self.upperHlBoxDiffPos[1]

    animate(self.upperHlBoxA, topleft=(x1,y1), duration=self.cursorAnimDur, tween=self.animTween)

    x2 = self.brHlBoxBasePos[0] + rx * self.brHlBoxDiffPos[0]
    y2 = self.brHlBoxBasePos[1] + ry * self.brHlBoxDiffPos[1]

    animate(self.brHlBoxA, topleft=(x2,y2), duration=self.cursorAnimDur, tween=self.animTween)

    if self.lastHighlightedCoord is not None:
      lx, ly = self.lastHighlightedCoord
      self.pmc.normalLightButton(lx,ly)
      self.pmc.highlightDict[lx][ly] = False
      dx, dy = lx-rx, ly-(ry+1)
    else: dx, dy = None, None

    self.lastHighlightedCoord=(rx, ry+1)
    self.pmc.highlightButton(  rx, ry+1)
    self.pmc.highlightDict[rx][ry] = True

    self.displayPoster(dx, dy)

  ###################### on key down ######################

  def on_key_down(self, key):
    if key == keys.RIGHT: self.shiftCursorRel( 1,  0)
    if key == keys.LEFT:  self.shiftCursorRel(-1,  0)
    if key == keys.UP:    self.shiftCursorRel( 0, -1)
    if key == keys.DOWN:  self.shiftCursorRel( 0,  1)

######################## main ######################## 
 
pb = posterBrowser()
  
pb.shiftCursorRel(0, 0) # temporary hack to highlight initial position

def draw(): 
  screen.clear()
  pb.draw()

def on_key_down(key): pb.on_key_down(key)

if pb.useMidiController:
  clock.schedule_interval(pb.poll, .05) #ask pygame to service midi polling

if pb.autoAdvanceSlides:
  clock.schedule_interval(pb.autoAdvancePosters, pb.cyclePosterFrequency)

### end ###
