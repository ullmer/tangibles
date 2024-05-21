# Successive illustrative examples of local & distributed (second) Wind
# Brygg Ullmer, Clemson University
# Begun 2024-05-20

WIDTH, HEIGHT = 1920, 1080
import pgzSetup #move window to 0,0 / top-left of screen; determine if opacity supported

wind  = Actor('wind21u3')
bldg1 = Actor('wind21j-bldg3', pos=(850, 450))
bldg2 = Actor('wind21s-bldg3', pos=(350, 650))

arrowTrans   = Actor('trans_arrows21v3')
#arrowsRot   = Actor('transArrows21v3')

actors       = [wind, bldg1, bldg2]
breezelets   = {}
breezeletCnt = 0
breezeFn     = 'wind21t-breeze3'
uiState      = {'current': None, 'translateActive': False, 'rotateActive': False,
                'translateFadeAnim': None}

#### draw ####

def draw(): 
  screen.clear()
  for a in actors:     a.draw()
  for b in breezelets: breezelets[b].draw()

  trActive, tfActive = uiState['translateActive'], uiState['translateFadeAnim']

  if trActive or (tfActive != None and tfActive.running): 
    if uiState['current'] != None: currentPos = uiState['current'].pos
    else:                          currentPos = uiState['lastActive'].pos
    arrowTrans.pos = currentPos
    arrowTrans.draw()

#### handle simple interactivity ####

def on_mouse_up():        
  uiState['lastActive'] = uiState['current']
  uiState['current']    = None

  if uiState['translateActive']:
    if pgzSetup.opacitySupported: 
      an = animate(arrowTrans, opacity=0., duration=0.5) #depends upon pgzero 1.3
      uiState['translateFadeAnim'] = an
    uiState['translateActive'] = False

def on_mouse_down(pos): 
  for a in actors:
    if a.collidepoint(pos): uiState['current'] = a

def on_mouse_move(pos, rel):
  dx, dy = rel

  for a in actors:
    if uiState['current'] == a:
      x1, y1 = a.pos

      #if a != 

      x2, y2 = x1+dx, y1+dy
      a.pos  = (x2, y2)
      if uiState['translateActive'] == False and uiState['current'] == wind:
        uiState['translateActive'] = True
        if pgzSetup.opacitySupported: 
          an = animate(arrowTrans, opacity=1., duration=0.25) #depends upon pgzero 1.3
          uiState['translateFadeAnim'] = an

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
