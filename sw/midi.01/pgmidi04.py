#!/usr/bin/env python

import sys, os, yaml
import pygame as pg
import pygame.midi

f = open('yaml/numark-dj2go-midi.yaml', 'rt')
y = yaml.safe_load(f)

#for el in y['mmpController']['controller']['controls']['control']: print(el['key'])

pg.init()
pygame.midi.init(); #print_device_info()

input_id = pygame.midi.get_default_input_id()
print("input_id:", input_id)

i = pygame.midi.Input(input_id)
print(i)

j = pygame.midi.get_device_info(1)
print(j)

#pg.display.set_mode((1, 1))

