#!/usr/bin/env python

import sys, os, yaml
import pygame as pg
import pygame.midi
from pygame import time 

f = open('yaml/numark-dj2go-midi.yaml', 'rt')
y = yaml.safe_load(f)

pygame.midi.init()
i = pygame.midi.Input(1)
o = pygame.midi.Output(4)
for i in range(64): o.note_on(i, i, 3)


#while True:
#  e = i.read(100); 

#  if len(e) > 0: 
#    for el in e: print(el)
#  else:          print(".", end=''); sys.stdout.flush()

#  time.delay(100)

### end ###
