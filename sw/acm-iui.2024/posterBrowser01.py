# Poster++ tangibles-supported browser code
# Brygg Ullmer, Clemson University
# Begun 2024-03-17

WIDTH  = 2160
HEIGHT = 2160

import moveWinHome #hack to move window to 0,0 on windows, avoiding redraw error
import pygame

class posterBrowser:
  topBlockFn   = 'full_res/top_block01'
  upperHlBoxFn = 'full_res/upper_highlight_box'

  topBlockPos         = (0, 0)
  upperHlBoxBasePos   = (13,218)
  upperHlBoxRelPos    = (0, 0)
  upperHlBoxRelMaxPos = (7, 7)
  hlBoxDiffPos        = (266, 196)
  animDur             = .3
  animTween           = 'accel_decel'

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

  ######################## constructActors ######################## 

  def constructActors(self):
    self.topBlockA   = Actor(self.topBlockFn,   topleft = self.topBlockPos)
    self.upperHlBoxA = Actor(self.upperHlBoxFn, topleft = self.upperHlBoxBasePos)

    self.actors = [self.topBlockA, self.upperHlBoxA]

  ######################## remove titlebar######################## 

  def removeTitlebar(self):
    self.scr = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    self.firstDraw = False
     
  ######################## draw ######################## 

  def draw(self):
    if self.firstDraw: self.removeTitlebar()
    for actor in self.actors: actor.draw()

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
    if key == keys.UP:    self.shiftUpperCursor( 0,  1)
    if key == keys.DOWN:  self.shiftUpperCursor( 0, -1)

######################## main ######################## 
 
pb = posterBrowser()

def draw(): 
  screen.clear()
  pb.draw()

def on_key_down(key): pb.on_key_down(key)

### end ###
