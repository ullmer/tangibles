# Non-uniform grid segmentation of image
# Brygg Ullmer, Clemson University
# Begun 2025-03-19

import glob, math, pygame
from enoButtonArray import *
from enoNUGrid      import *
from pgzero.builtins import Actor, animate, keyboard

WIDTH, HEIGHT = 1920, 1080

#################### generate images list ####################

class enoPgzGridSeg(enoNUGrid): 

  baseImg            = None
  actorHandle        = None

  lastObjSelected      = None
  lastSelectionDetails = None

  lineColor           = (255,255,255)
  cornerColor         = (255,255,  0)
  coordRad            = 10 #coordinate radius
  cornerSelected      = None
  sideSelected        = None # if selected, assigned a pair: side, then index
  verbose             = True
  nudge               = 4 #pixel value for shifting

  fontSize = 40 
  fgcolor  = (150, 150, 50)
  bgcolor  = (100, 100, 100)
  alpha    = .7

  #################### constructor ####################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)
    super().__init__()

    if self.baseImg  is not None: self.actorHandle = Actor(self.baseImg)
    if self.cornerCoords is None: self.setDefaultCoords()

  #################### message ####################

  def msg(self, msgStr): print("enoPgzGridSeg msg: " + str(msgStr))

  #################### draw ####################

  def draw(self, screen):
    screen.clear()
    if self.actorHandle  is not None: self.actorHandle.draw()
    if self.cornerCoords is not None: self.drawSegMatrix(screen)

  #################### draw coordinate circle ####################

  def drawCoordCirc(self, screen, coord): screen.draw.circle(coord, self.coordRad, self.cornerColor)

  def interpolateCoord(self, a, b, p):
    x1, y1 = a; x2, y2 = b
    x = x1 + p * (x2 - x1)
    y = y1 + p * (y2 - y1)
    return (x, y)

  #################### draw segmention matrix ####################

  def drawSegMatrix(self, screen):

    c1, c2, c3, c4 = self.cornerCoords
    ndx1, ndy1 = self.numDivsX+1, self.numDivsY+1 

    x1span = c2[0] - c1[0]; dx1 = x1span / ndx1; x2span = c4[0] - c3[0]; dx2 = x2span / ndx1
    x3span = c3[0] - c1[0]; dx3 = x3span / ndx1; x4span = c4[0] - c2[0]; dx4 = x4span / ndx1

    y1span = c3[1] - c1[1]; dy1 = y1span / ndy1; y2span = c4[1] - c2[1]; dy2 = y2span / ndy1
    y3span = c2[1] - c1[1]; dy3 = y3span / ndy1; y4span = c4[1] - c3[1]; dy4 = y4span / ndy1

    #if self.verbose: print("spans:", str([x1span, x2span, y1span, y2span]))

    lc = self.lineColor; cc = self.cornerColor; s = screen

    #s.draw.line(c1, c2, lc); s.draw.line(c2, c4, lc); s.draw.line(c3, c4, lc); s.draw.line(c3, c1, lc)
    for c in self.cornerCoords: self.drawCoordCirc(screen, c)

    ndx1 = self.numDivsX + 1; ndy2 = self.numDivsY + 1

    for idx in range(ndx1):
      xd1, xd2 = self.topDivs[idx],   self.bottomDivs[idx]

      l1 = self.interpolateCoord(c1, c2, xd1)
      l2 = self.interpolateCoord(c3, c4, xd2)

      s.draw.line(l1, l2, lc);        idx+=1
      self.drawCoordCirc(screen, l1); self.drawCoordCirc(screen, l2)
      self.topVertices[idx] = l1;     self.bottomVertices[idx] = l2

      #if self.verbose: print("xd l1 l2: ", str(xd1), str(xd2), str(l1), str(l2))

    for idx in range(ndy1):
      yd1, yd2 = self.leftDivs[idx],  self.rightDivs[idx]
      l1 = self.interpolateCoord(c1, c3, yd1)
      l2 = self.interpolateCoord(c2, c4, yd2)

      s.draw.line(l1, l2, lc);        idx+=1
      self.drawCoordCirc(screen, l1); self.drawCoordCirc(screen, l2)
      self.leftVertices[idx] = l1;    self.rightVertices[idx] = l2

      #if self.verbose: print("yd l1 l2: ", str(yd), str(l1), str(l2))

    self.highlightSectorCoords(screen, 2, 2)
    self.labelSectors(screen)

  #################### highlightSectorCoords ####################

  def highlightSectorCoords(self, screen, x, y):
    sc = self.getSectorCoords(x, y)
    for coord in sc: self.drawCoordCirc(screen, coord)

  def drawSectorBoundingBoxe(self, screen, x, y):
    a,b,c,d = self.getSectorCoords(x, y)
    tl, br  = getBoundingBox(a,b,c,d)
    w, h    = abs(br[0] - tl[0]), abs(br[1] - tl[1])

    r = Rect(tl, (w, h))
    screen.draw.rect(r, self.bgcolor)

  #################### label sectors ####################

  def labelSectors(self, screen):
    try:
      for j in range(self.numDivsX):
        for i in range(self.numDivsY):
          sc = self.getSectorCoords(i, j)
          if sc is None: continue #revisit+fix!
          a,b,c,d = sc
          x, y    = getCoordAvg1(a,b,c,d)

          ordA     = ord('A')
          labelStr = chr(ordA + j) + str(i)

          screen.draw.text(labelStr, centerx=x, centery=y, align="center",
            fontsize=self.fontSize, color=self.fgcolor, alpha=self.alpha)

          self.drawSectorBoundingBoxe(screen, i, j)

    except: self.err("labelSectors")

  #################### handle mouse press event ####################

  def on_mouse_down(self, pos): 
    for i in range(4):
      corner = self.cornerCoords[i]
      dist   = math.dist(pos, corner)
      if dist < self.coordRad: 
        self.cornerSelected = i; return

    #print(str(self.sideVertexHandles))

    for side in self.sideVertexHandles:
      vertices = self.sideVertexHandles[side]
      for idx in vertices:
        vertex = vertices[idx]
        dist   = math.dist(pos, vertex)
        if dist < self.coordRad: 
          self.sideSelected = (side, idx)
          #if self.verbose: print("on_mouse_down sideSelected: " + str(self.sideSelected), str(vertices), str(idx), str(dist))
          return

  #################### handle mouse move event ####################

  def on_mouse_move(self, pos, rel): 

    if self.cornerSelected is not None: 
      cx, cy = self.cornerCoords[self.cornerSelected]
      dx, dy = rel
      self.cornerCoords[self.cornerSelected] = (cx+dx, cy+dy)

    if self.sideSelected is not None:
      #if self.verbose: print("on_mouse_move sideSelected: " + str(self.sideSelected))

      side, idx = self.sideSelected; idx -= 1
      dx, dy    = rel
      c1, c2, c3, c4 = self.cornerCoords

      origNormPos = self.divsEnsemble[side][idx]
   
      #on widely-deployed raspberry pi raspbian bullseye distro, default python is 3.9.2; 
      #  match/switch introduced in 3.10.  sigh

      if   side == "left":   fullspan = c3[1] - c1[1]; relNormChange = float(dy) / float(fullspan)
      elif side == "right":  fullspan = c4[1] - c2[1]; relNormChange = float(dy) / float(fullspan)
      elif side == "top":    fullspan = c2[0] - c1[0]; relNormChange = float(dx) / float(fullspan)
      elif side == "bottom": fullspan = c4[0] - c3[0]; relNormChange = float(dx) / float(fullspan)
      else:                  self.msg("on_mouse_move unexpected state 2"); return
 
      newNormPos = origNormPos + relNormChange
      self.divsEnsemble[side][idx] = newNormPos

  #################### on mouse up ####################

  def on_mouse_up(self): 
    if self.cornerSelected is None and self.sideSelected is not None:
      self.lastObjSelected = 'side'
      self.lastSelectionDetails = self.sideSelected
    
    if self.cornerSelected is not None and self.sideSelected is None:
      self.lastObjSelected = 'corner'
      self.lastSelectionDetails = self.cornerSelected
    
    if self.cornerSelected is None and self.sideSelected is not None:
      self.lastObjSelected = 'side'
    
    self.cornerSelected = None; self.sideSelected = None
    if self.verbose: self.printYaml()
    print("")

  #################### nudge corner ####################

  def nudgeCorner(self, cornerIdx,  dx, dy):
    x1, y1 = self.getCornerCoord(cornerIdx)
    x2, y2 = x1+dx, y1+dy
    self.setCornerCoord(cornerIdx, (x2, y2))

  #################### on key down####################

  def on_key_down(self, key): 
    if self.lastObjSelected == 'corner':
      cornerIdx = self.lastSelectionDetails

      if key == keys.UP:    self.nudgeCorner(cornerIdx, 0,  self.nudge)
      if key == keys.DOWN:  self.nudgeCorner(cornerIdx, 0, -self.nudge)
      if key == keys.LEFT:  self.nudgeCorner(cornerIdx, -self.nudge, 0)
      if key == keys.RIGHT: self.nudgeCorner(cornerIdx,  self.nudge, 0)
    
#################### main ####################

if __name__ == "__main__":

  buttons = ['save', 'load']
 
  epgs = enoPgzGridSeg(baseName='tbt28j', baseImg='tbt28j/0001')
  eba  = enoButtonArray(labelArray=buttons, basePos=(100, 100), dx=0, dy=35)
 
  def draw():                  epgs.draw(screen); eba.draw(screen)
  def on_mouse_down(pos):      epgs.on_mouse_down(pos); eba.on_mouse_down(pos)
  def on_mouse_move(pos, rel): epgs.on_mouse_move(pos, rel)
  def on_mouse_up():           epgs.on_mouse_up()
 
  def buttonCB(cmd): 
    if cmd == 'save': epgs.saveYaml()
    if cmd == 'load': epgs.loadYaml()
 
  eba.addCallback(buttonCB)
 
### end ###
