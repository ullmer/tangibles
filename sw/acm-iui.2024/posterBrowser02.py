# Poster++ tangibles-supported browser code
# Brygg Ullmer, Clemson University
# Begun 2024-03-17

import moveWinHome #hack to move window to 0,0 on windows, avoiding redraw error

WIDTH  = 2160
HEIGHT = 3660

import pygame
from posterMidi        import *
from enoMidiController import *

class posterBrowser:
  topBlockFn   = 'full_res/top_block01'
  upperHlBoxFn = 'full_res/upper_highlight_box'

  topBlockPos          = (0, 0)
  upperHlBoxBasePos    = (13,218)
  upperHlBoxRelPos     = (0, 0)
  upperHlBoxRelMaxPos  = (7, 7)
  hlBoxDiffPos         = (266, 183)
  lastHighlightedCoord = None

  posterFullPos       = (0,  1210)
  animDur             = .3
  animTween           = 'accel_decel'
  removeTitle         = True

  useMidiController   = True
  emc                 = None #enodia midi  controller handle
  pmc                 = None #enodia poster midi controller handle

  numPosters          = 34
  posterFnPrefix      = 'posters.0315a/screen_res/iui24_'
  posterActors        = None
  activePoster         = 1
  cyclePosters         = True #automatically cycle between posters
  cyclePosterFrequency = 10.  #how frequently to make the cycling
  cyclePosterAutolaunchDelay = 60. #after how many seconds should autolaunch begin

  topBlockA    = None #pgzero actors
  upperHlBoxA  = None

  firstDraw    = True 

  arrayDim = [8, 8]

  actors   = None
  scr      = None
  verbose  = True

  ######################## constructor ######################## 

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.constructActors()

    if self.useMidiController: self.launchMidiController()

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

    a   = Actor(afn, topleft=self.posterFullPos)
    self.posterActors[whichPoster] = a
    return a

  ######################## constructActors ######################## 

  def constructActors(self):
    self.topBlockA   = Actor(self.topBlockFn,   topleft = self.topBlockPos)
    self.upperHlBoxA = Actor(self.upperHlBoxFn, topleft = self.upperHlBoxBasePos)

    self.posterActors = {}

    self.actors = [self.topBlockA, self.upperHlBoxA]

  ######################## remove titlebar######################## 

  def removeTitlebar(self):
    self.scr = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    pygame.display.toggle_fullscreen()
    self.firstDraw = False
     
  ######################## draw ######################## 

  def draw(self):
    if self.firstDraw and self.removeTitle: self.removeTitlebar()
    for actor in self.actors: actor.draw()

    pa = self.getPosterActor(self.activePoster)
    pa.draw()

  ###################### shiftCursor ######################

  def shiftCursorRel(self, dx, dy): 
    rx, ry = self.upperHlBoxRelPos
    relmax = self.upperHlBoxRelMaxPos 

    if   dy + ry < 0:         ry = relmax[1]
    elif dy + ry > relmax[1]: ry = 0
    else:                     ry += dy

    if   dx + rx < 0:         rx = 0
    elif dx + rx > relmax[0]: rx = 0; ry += 1
    else:                     rx += dx

    self.upperHlBoxRelPos = (rx, ry)

    x = self.upperHlBoxBasePos[0] + rx * self.hlBoxDiffPos[0]
    y = self.upperHlBoxBasePos[1] + ry * self.hlBoxDiffPos[1]

    animate(self.upperHlBoxA, topleft=(x,y), duration=self.animDur, tween=self.animTween)

    lx, ly = self.lastHighlightedCoord
    self.pmc.normalLightButton(lx,ly)
    self.pmc.highlightDict[lx][ly] = False

    self.lastHighlightedCoord=(rx, ry+1)
    self.pmc.highlightButton(  rx, ry+1)
    self.pmc.highlightDict[rx][ry] = True

  ###################### shiftCursor ######################

  def shiftCursorAbs(self, rx, ry): 

    self.upperHlBoxRelPos = (rx, ry)

    x = self.upperHlBoxBasePos[0] + rx * self.hlBoxDiffPos[0]
    y = self.upperHlBoxBasePos[1] + ry * self.hlBoxDiffPos[1]

    animate(self.upperHlBoxA, topleft=(x,y), duration=self.animDur, tween=self.animTween)

  ###################### on key down ######################

  def on_key_down(self, key):
    if key == keys.RIGHT: self.shiftCursorRel( 1,  0)
    if key == keys.LEFT:  self.shiftCursorRel(-1,  0)
    if key == keys.UP:    self.shiftCursorRel( 0, -1)
    if key == keys.DOWN:  self.shiftCursorRel( 0,  1)
    selPosterNum = self.calcSelectedPoster() 
    print("selected poster number:", selPosterNum)
    self.activePoster = selPosterNum

######################## main ######################## 
 
pb = posterBrowser()

def draw(): 
  screen.clear()
  pb.draw()

def on_key_down(key): pb.on_key_down(key)

if pb.useMidiController:
  clock.schedule_interval(pb.poll, .05) #ask pygame to service midi polling

### end ###
