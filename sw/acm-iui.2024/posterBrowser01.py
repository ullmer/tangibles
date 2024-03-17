# Poster++ tangibles-supported browser code
# Brygg Ullmer, Clemson University
# Begun 2024-03-17

import moveWinHome #hack to move window to 0,0 on windows, avoiding redraw error

WIDTH  = 2160
HEIGHT = 3660

import pygame

class posterBrowser:
  topBlockFn   = 'full_res/top_block01'
  upperHlBoxFn = 'full_res/upper_highlight_box'

  topBlockPos         = (0, 0)
  upperHlBoxBasePos   = (13,218)
  upperHlBoxRelPos    = (0, 0)
  upperHlBoxRelMaxPos = (7, 7)
  hlBoxDiffPos        = (266, 183)
  posterFullPos       = (0,  1210)
  animDur             = .3
  animTween           = 'accel_decel'
  removeTitle         = True

  numPosters          = 34
  posterFnPrefix      = 'posters.0315a/screen_res/iui24_'
  posterActors        = None
  activePoster         = 0
  cyclePosters         = True #automatically cycle between posters
  cyclePosterFrequency = 10.  #how frequently to make the cycling
  cyclePosterAutolaunchDelay = 60. #after how many seconds should autolaunch begin

  topBlockA    = None #pgzero actors
  upperHlBoxA  = None

  firstDraw    = True 

  arrayDim = [8, 8]

  actors   = None
  scr      = None

  ######################## constructor ######################## 

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.constructActors()

  ######################## calcSelectedPoster ######################## 

  def calcSelectedPoster(self): 
    rx, ry = self.upperHlBoxRelPos
    mx, my = self.upperHlBoxRelMaxPos
    result = rx + ry * mx
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

  ###################### shiftUpperCursor ######################

  def shiftUpperCursor(self, dx, dy): 
    uhbrp  = self.upperHlBoxRelPos
    uhbrmp = self.upperHlBoxRelMaxPos 

    rx, ry = uhbrp

    if   dx + uhbrp[0] < 0:         rx = 0
    elif dx + uhbrp[0] > uhbrmp[0]: rx = uhbrmp[0]
    else:                           rx += dx

    if   dy + uhbrp[1] < 0:         ry = 0
    elif dy + uhbrp[1] > uhbrmp[1]: ry = uhbrmp[1]
    else:                           ry += dy

    self.upperHlBoxRelPos = (rx, ry)

    x = self.upperHlBoxBasePos[0] + uhbrp[0] * self.hlBoxDiffPos[0]
    y = self.upperHlBoxBasePos[1] + uhbrp[1] * self.hlBoxDiffPos[1]

    #self.upperHlBoxA.topleft = (x, y)
    animate(self.upperHlBoxA, topleft=(x,y), duration=self.animDur, tween=self.animTween)

  ###################### on key down ######################

  def on_key_down(self, key):
    if key == keys.RIGHT: self.shiftUpperCursor( 1,  0)
    if key == keys.LEFT:  self.shiftUpperCursor(-1,  0)
    if key == keys.UP:    self.shiftUpperCursor( 0, -1)
    if key == keys.DOWN:  self.shiftUpperCursor( 0,  1)
    selPosterNum = self.calcSelectedPoster()
    print("selected poster number:", selPosterNum)

######################## main ######################## 
 
pb = posterBrowser()

def draw(): 
  screen.clear()
  pb.draw()

def on_key_down(key): pb.on_key_down(key)

### end ###
