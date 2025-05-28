#!/usr/bin/env python

import sys, os

import pygame as pg
import pygame.midi

def gatherMidiDeviceInfo():
  result = {}
  for i in range(pygame.midi.get_count()):
    r = pygame.midi.get_device_info(i)
    (interf, name, input, output, opened) = r

    in_out = ""

    if input:  in_out = "(input)"
    if output: in_out = "(output)"

    entry = {}
    entry['interface'] = interf
    entry['name']      = name
    result[i] = entry
  return result

pg.init()
pygame.midi.init()
mdi  = gatherMidiDeviceInfo()
print(mdi)

pygame.midi.quit()

#pg.display.set_mode((1, 1))

