# Enodia pgzero-xi slider
# By Brygg Ullmer, Clemson University
# Begun 2022-07-23

from   pgzEno import *
from   pgzero.builtins import Actor

#####################################################
#################### pgze slider ####################
#####################################################

class pgzeSlider:

  sliderBaseFn     = 'slider_base01'
  sliderCursorFn   = 'slider_cursor02'
  sliderGlyphRotFn = 'slider_glyph_rot01'
  sliderGlyphFn    = None

  sliderBaseA, sliderCursorA, sliderGlyphA = [None]*3 #Actor handles
  actors           = None
  touch_coords     = None

  glyphRelPos       = [ 0, -115]
  cursorRelBasePos  = [ 0,  -77]
  sliderVizPos      = [50,   50]  #overall visual repr; not valuator itself

  cursorMinPosY     =  55  # minimum pixel-value y offset, vert-oriented slider
  cursorMaxPosY     =  285 # maximum pixel-value y offset, vert-oriented slider
  cursorCurrentPos  = 0 # current pixel-value y offset 
  cursorMinMaxRange = cursorMaxPosY - cursorMinPosY

  cursorCurrentVal = 0
  cursorMinVal     = 1
  cursorMaxVal     = 100
  verbose          = False

  ######################### constructor #########################

  def __init__(self, pos, glyphImgFn=None):
    if glyphImgFn == None: self.sliderGlyphFn = self.sliderGlyphRotFn
    else:                  self.sliderGlyphFn = glyphImgFn

    if pos != None: self.sliderVizPos = pos

    self.buildSlider()

  ######################### build slider #########################

  def buildSlider(self):

    bx,  by  = bpos = self.sliderVizPos #base x/y positions
    cdx, cdy = self.cursorRelBasePos    #cursor relative base position
    gdx, gdy = self.glyphRelPos         #glyph relative position

    cpos = bx + cdx, by + cdy
    gpos = bx + gdx, by + gdy

    b = self.sliderBaseA   = Actor(self.sliderBaseFn,   bpos)
    c = self.sliderCursorA = Actor(self.sliderCursorFn, cpos)
    g = self.sliderGlyphA  = Actor(self.sliderGlyphFn,  gpos)

    self.actors       = [b,c,g]
    self.touch_coords = {}
    
  ######################### draw #########################

  def draw(self):
    for actor in self.actors: actor.draw()

  ############ normalize position ##########

  def normalizePos(self, x, y): 
    global WIDTH, HEIGHT
    return (int(x*WIDTH), int(y*HEIGHT))

  ##################### calculate normalized position #####################

  def calcNormVal(self, pixelY):
    svpy   = self.sliderVizPos[1]
    relY   = pixelY-svpy #normalizes out Y offset of slider representation
    minY   = self.cursorMinPosY
    rangeY = self.cursorMinMaxRange 
    result = (relY - minY)/rangeY
    if result > 1.: result = 1.
    return result

  ######################### on_mouse_down #########################

  def on_finger_down(self, finger_id, x, y):
    if self.verbose: print("ofd:", x, y)
    b = self.sliderBaseA   

    if b.collidepoint((x,y)): 
      bx = self.sliderVizPos[0]
      self.sliderCursorA.pos=(bx, y)
      normVal = self.calcNormVal(y)
      if self.verbose: print(normVal)
      return True

    return False

  ############ fingermove ##########
  
  def on_finger_move(self, finger_id, x, y):
    self.on_finger_down(finger_id, x, y)
  
  ################### "mouse" events ###################
  
  def on_mouse_up(self, pos):
    self.touch_coords.clear()
    #print("mouse UP")
  
### end ###
