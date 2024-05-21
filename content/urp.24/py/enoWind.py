# Class providing initial Wind support
# Brygg Ullmer, Clemson University
# Begun 2024-05-21

import math
from pgzero.builtins import Actor, animate, keyboard

class enoWind(Actor):
  windImgFn    = 'wind21u3'
  arrowTransFn = 'trans_arrows21v3'
  arrowRotFn   = 'rot_arrows21y3'
  breezeImgFn  = 'wind21t-breeze3'

  arrowTrans   = None
  arrowRot     = None

  translateActive    = False
  rotateActive       = False
  translateFadeAnim  = None
  rotateFadeAnim     = None

  breezeGenFrequency = 2.
  breezeletDuration  = 9.
  fadeInDuration     = .25
  fadeOutDuration    = .5

  breezelets   = None
  breezeletCnt = 0

  windDistanceTransRotThresh = 75

  opacitySupported  = False  # hope this will be overridden, but -- if we expect it and unsupported,
                             # potential for crash, re dependency upon pgzero >=1.3

  #### constructor ####

  def __init__(self, coreImageFn=None, **kwargs):

    self.__dict__.update(kwargs)        #allow class fields to be passed in constructor
    if coreImageFn == None: coreImageFn = self.windImgFn
    super().__init__(coreImageFn)       #pass core image filename to Actor ~parent-class

    self.arrowTrans = Actor(self.arrowTransFn)
    self.arrowRot   = Actor(self.arrowRotFn)
    self.breezelets = {}

  #### draw ####
 
  def draw(self): 
    super().draw()
 
    trActive, tfActive = self.translateActive, self.translateFadeAnim
  
    if trActive or (tfActive != None and tfActive.running): 
      self.arrowTrans.pos = self.pos
      self.arrowTrans.draw()
 
    rotActive, rfActive = self.rotateActive, self.rotateFadeAnim
 
    if rotActive or (rfActive != None and rfActive.running): 
      self.arrowRot.pos = self.pos
      self.arrowRot.draw()

    for b in self.breezelets: self.breezelets[b].draw()
 
  #### mouse press ####
 
  def on_mouse_down(self, pos): 
 
    distanceFromWindCenter = math.dist(pos, self.pos)
 
    if distanceFromWindCenter > self.windDistanceTransRotThresh: #rotation mode
      self.rotateActive = True
      if self.opacitySupported: 
        an = animate(self.arrowRot, opacity=1., duration=self.fadeInDuration) 
        self.rotFadeAnim = an
    else: 
      self.translateActive = True
      if self.opacitySupported: 
        an = animate(self.arrowTrans, opacity=1., duration=self.fadeInDuration)
        self.translateFadeAnim = an
 
  #### mouse release ####
 
  def on_mouse_up(self):
 
    if self.translateActive:
      if self.opacitySupported: 
        an = animate(self.arrowTrans, opacity=0., duration=self.fadeOutDuration) 
        self.translateFadeAnim = an
      self.translateActive = False
 
    if self.rotateActive:
      if self.opacitySupported: 
        an = animate(self.arrowRot, opacity=0., duration=self.fadeOutDuration) 
        self.rotateFadeAnim = an
      self.rotateActive     = False
      
  #### calculate wind rotation ####
 
  def calcWindRotRel(self, windPos, pos, rel):
 
    wpx, wpy = windPos
    px,  py  = pos
    rx,  ry  = rel
  
    dx1, dy1 = px-wpx, py-wpy
    dx2, dy2 = rx-wpx, ry-wpy
 
    angle1 = math.atan2(dy1, dx1) 
    angle2 = math.atan2(dy2, dx2) 
 
    a = angle2 - angle1
 
    #print(angle2, angle1, a)
 
    return angle1 # this is not correct value, but a semi-functional placeholder
      
  #### mouse movement ####
 
  def on_mouse_move(self, pos, rel):
    dx, dy = rel
 
    if self.rotateActive:
      self.angle += self.calcWindRotRel(wind.center, pos, rel)
      return
 
  #### breeze ~engine ####
 
  def genBreezelet(self):
    b = Actor(self.breezeImgFn, pos=self.pos)
 
    x1, y1 = b.pos
    x2     = x1 + 1524 
 
    animate(b, pos=(x2, y1), duration=self.breezeletDuration)
 
    breezelets[breezeletCnt] = b #use of a dictionary will help with cleanup 
    breezeletCnt += 1
 
  #### breeze ~engine ####
 
  def startBreeze(self):
    self.genBreezelet()
    clock.schedule_interval(self.genBreezelet, self.breezeGenFrequency)
 
### end ###
