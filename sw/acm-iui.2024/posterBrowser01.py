# Poster++ tangibles-supported browser code
# Brygg Ullmer, Clemson University
# Begun 2024-03-17

WIDTH  = 2160
HEIGHT = 2160

class posterBrowser:
  topBlockFn   = 'full_res/top_block01'
  upperHlBoxFn = 'full_res/upper_highlight_box'

  topBlockPos   = (0,0)
  upperHlBoxPos = (0,0)

  topBlockA    = None #pgzero actors
  upperHlBoxA  = None

  arrayDim = [8, 8]

  actors   = None

  ######################## constructor ######################## 

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.constructActors()

  ######################## constructActors ######################## 

  def constructActors(self):
    self.topBlockA   = Actor(self.topBlockFn,   pos = self.topBlockPos)
    self.upperHlBoxA = Actor(self.upperHlBoxFn, pos = self.upperHlBoxPos)

    self.actors = [self.topBlockA, self.upperHlBoxA]
     
  ######################## draw ######################## 

  def draw(self):
    for actor in self.actors: actor.draw()

######################## main ######################## 
 
pb = posterBrowser()

def draw(): 
  screen.clear()
  pb.draw()

### end ###
