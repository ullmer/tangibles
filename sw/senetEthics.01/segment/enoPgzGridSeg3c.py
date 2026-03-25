# Non-uniform grid segmentation of image
# Brygg Ullmer, Clemson University

# Begun 2025-03-19

import glob, math, pygame

from enoButtonArray import *
from enoNUGrid      import *
from enoPgzGridSeg3 import *

WIDTH, HEIGHT = 1920, 1080

#################### main ####################

actions = ['save',     'load',   'shard']
data    = ['senet03k']

#epgs = enoPgzGridSeg(baseName='tbt28j20', baseImg='tbt28j/0020lh')
epgs = enoPgzGridSeg(baseName='senet03k', baseImg='senet03k.png', numDivsX=3, numDivsY=10)
ebaa = enoButtonArray(labelArray=actions, basePos=(30, 30), dx=0, dy=35)
ebad = enoButtonArray(labelArray=data,    basePos=(130,30), dx=0, dy=35)

def draw():                  
  for obj in [epgs, ebaa, ebad]: obj.draw(screen)

def on_mouse_down(pos):      
  for obj in [epgs, ebaa, ebad]: obj.on_mouse_down(pos)

def on_mouse_up():           
  for obj in [epgs, ebaa, ebad]: obj.on_mouse_up()

def on_mouse_move(pos, rel): epgs.on_mouse_move(pos, rel)

def on_key_down(key): 
  for obj in [epgs, ebaa, ebad]: obj.on_key_down(key)

def actionsCB(cmd): 
  if cmd == 'save':  epgs.saveYaml()
  if cmd == 'load':  epgs.loadYaml()
  if cmd == 'shard': epgs.shardSectors()

ebaa.addCallback(actionsCB)

### end ###
