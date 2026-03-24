# Broad contours of "key objects of interest" toward
#  Computing, Ethics, and Global Society example
# Brygg Ullmer, Clemson Universty
# Begun 2026-03-24

from ataBase import *

class EnoTok(AtaBase):
  def draw():   pass
  def update(): pass

  def on_mouse_down(pos):    pass
  def on_key_down(key, mod): pass

class EnoPeople(enoTok):
  name, abbrev, era, domains, themes, colors, notes = [None]*7

class EnoTheme(enoTok):
  name, color, themes = [None]*3

### end ###
