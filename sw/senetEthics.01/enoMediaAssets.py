# Enodia Backdrops
# Brygg Ullmer, Clemson University
# Begun 2026-03-28

import yaml
from pgzero.builtins import Actor, animate, keyboard, keys

from enoActor        import *
from enoOSsupport    import *

################### Enodia People Yaml Mixin ###################

class EnoBackdropsPgz:
  actors           = None # type: dict[Actor]|None
  imagesSubpath    = "images/"
  backdropsSubpath = "backdrops/"
  backdropsYamlFn  = "yaml/backdrops.yaml"

  basePos = (0, 0)
  selectedActor   = None

  ############# build people #############

  def buildActors(self):
    try:    
      pif = self.pgzImagesPrefix
      self.actors = []
      x, y = self.basePos
      abbrevs = self.getAbbrevs()

      for pa in abbrevs:
        fn = self.peoplePathPrefix + pa.lower()
        if filepatExists(pif+fn):
          try:    a  = Actor(fn) 
          except: self.msg("buildActors: problem with "+pa); continue
        else: self.msg("File " + pa + " does not exist; ignoring"); continue

        self.actors.append(a)
        a.pos = (x, y); x += self.dx 
        
    except: self.err("buildActors")

  ############# draw #############

  def draw(self):
    try:    
      for a in self.actors: a.draw()
    except: self.err("draw")

  ############# on_mouse_down #############

  def on_mouse_down(self, pos): 
    try:    
      for a in self.actors:
        if a.collidepoint(pos): 
          self.selectedActor = a
    except: self.err("on_mouse_down")

  ############# on_mouse_down #############

  def on_mouse_up(self): 
    try:    
      animate(self.selectedActor, pos=(100,100), tween='accel_decel')
      self.selectedActor = None
    except: self.err("on_mouse_up")

  ############# on_mouse_move #############

  def on_mouse_move(self, rel):
    try:    
      if self.selectedActor is not None: 
        dx, dy = rel
        x,  y  = self.selectedActor.pos
        x += dx; y += dy
        self.selectedActor.pos = (x,y)
    except: self.err("on_mouse_up")

####################################################
################### Enodia Theme ###################

class EnoThemeMixinPgz:
  def draw(self): pass

################### Enodia Themes ###################

class EnoThemesMixinPgz:
# themes = None # type: list[EnoTheme]

  def draw(self):
    try:    
      for theme in self.themes: theme.draw()
    except: self.err("draw")

### end ###


backdrops:
  chessSA1:
    url:   https://computing.clemson.edu/~bullmer/images/chessSofonisbaAnguissola1555o.jpg
    local: chessSofonisbaAnguissola1555o.jpg

  chessSA1:
    local: senet03k.png

### end ###
yaml/backdrops.yaml
