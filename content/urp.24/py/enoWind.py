# Class providing initial Wind support
# Brygg Ullmer, Clemson University
# Begun 2024-05-21

import pgzSetup #move window to 0,0 / top-left of screen; determine if opacity supported
import math
from pgzero.builtins import Actor, animate, keyboard

class enoWind(Actor):
  coreimageFn = 'wind21u3'

  arrowTrans = Actor('trans_arrows21v3')
  arrowRot   = Actor('rot_arrows21y3')

  translateActive   = False
  rotateActive      = False
  translateFadeAnim = None
  rotateFadeAnim    = None

  ##constructor ###

  def __init__(self, coreImageFn=None):
    if coreImageFn == None: coreImageFn = self.windImageFn
    super().__init__(coreImageFn)

  #### draw ####

  def draw(self): 

    trActive, tfActive = uiState['translateActive'], uiState['translateFadeAnim']
  
    if trActive or (tfActive != None and tfActive.running): 
      if uiState['current'] != None: currentPos = uiState['current'].pos
      else:                          currentPos = uiState['lastActive'].pos
      arrowTrans.pos = currentPos
      arrowTrans.draw()

    rotActive, rfActive = uiState['rotateActive'], uiState['rotateFadeAnim']

  if rotActive or (rfActive != None and rfActive.running): 
    if uiState['current'] != None: currentPos = uiState['current'].pos
    else:                          currentPos = uiState['lastActive'].pos
    arrowRot.pos = currentPos
    arrowRot.draw()

#### mouse press ####

def on_mouse_down(pos): 
  for a in actors:
    if a.collidepoint(pos): uiState['current'] = a

  if uiState['current'] == wind:
    distanceFromWindCenter = math.dist(pos, wind.pos)

    if distanceFromWindCenter > 75: #rotation mode
      uiState['rotateActive'] = True
      if pgzSetup.opacitySupported: 
        an = animate(arrowRot, opacity=1., duration=0.25) #depends upon pgzero 1.3
        uiState['rotFadeAnim'] = an
    else: 
      uiState['translateActive'] = True
      if pgzSetup.opacitySupported: 
        an = animate(arrowTrans, opacity=1., duration=0.25) #depends upon pgzero 1.3
        uiState['translateFadeAnim'] = an

#### mouse release ####

def on_mouse_up():        
  uiState['lastActive'] = uiState['current']
  uiState['current']    = None

  if uiState['translateActive']:
    if pgzSetup.opacitySupported: 
      an = animate(arrowTrans, opacity=0., duration=0.5) #depends upon pgzero 1.3
      uiState['translateFadeAnim'] = an
    uiState['translateActive'] = False

  if uiState['rotateActive']:
    if pgzSetup.opacitySupported: 
      an = animate(arrowRot, opacity=0., duration=0.5) #depends upon pgzero 1.3
      uiState['rotateFadeAnim'] = an
    uiState['rotateActive'] = False
    
#### calculate wind rotation ####

def calcWindRotRel(windPos, pos, rel):

  wpx, wpy = windPos
  px,  py  = pos
  rx,  ry  = rel

  dx1, dy1 = px-wpx, py-wpy
  dx2, dy2 = rx-wpx, ry-wpy

  angle1 = math.atan2(dy1, dx1) 
  angle2 = math.atan2(dy2, dx2) 

  a = angle2 - angle1

  #print(angle2, angle1, a)

  return angle1
      
#### mouse movement ####

def on_mouse_move(pos, rel):
  dx, dy = rel

  if uiState['current'] == wind and uiState['rotateActive']:
    wind.angle += calcWindRotRel(wind.center, pos, rel)
    return

  for a in actors:
    if uiState['current'] == a:
      x1, y1 = a.pos

      x2, y2 = x1+dx, y1+dy
      a.pos  = (x2, y2)

#### breeze ~engine ####

def genBreezelet():
  global breezeletCnt
  b = Actor(breezeFn, pos=wind.pos)

  x1, y1 = b.pos
  x2     = x1 + 1524 

  animate(b, pos=(x2, y1), duration=9.)

  breezelets[breezeletCnt] = b #use of a dictionary will help with cleanup 
  breezeletCnt += 1

genBreezelet()
clock.schedule_interval(genBreezelet, 2)

### end ###
