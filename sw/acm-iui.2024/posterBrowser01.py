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

  topBlockPos   = (0,0)
  upperHlBoxPos = (0,0)

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
    self.upperHlBoxA = Actor(self.upperHlBoxFn, topleft = self.upperHlBoxPos)

    self.actors = [self.topBlockA, self.upperHlBoxA]

  ######################## remove titlebar######################## 

  def removeTitlebar(self):
    self.scr = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    self.firstDraw = False
     
  ######################## draw ######################## 

  def draw(self):
    if self.firstDraw: self.removeTitlebar()
    for actor in self.actors: actor.draw()

######################## main ######################## 
 
pb = posterBrowser()

def draw(): 
  screen.clear()
  pb.draw()

### end ###
