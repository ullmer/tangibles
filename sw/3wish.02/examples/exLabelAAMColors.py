# Code to manually assign colors for chosen YAML-sourced value sequence
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import yaml
import enoFcTkMidi 

yfn = 'cuColleges01.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

#print(yd)

im  = yd['imageMatrix']
mm  = im['matrixMap']

basedir = enoFcTkMidi.basedir
eftm = enoFcTkMidi.enoFcTkMidi(swBasePath=basedir)

enoFcTkMidi.tkMain()

for key in mm:
  mmkEl  = mm[key]
  mmkEl0 = mmkEl[0]
  print(key, mmkEl0)

#imageMatrix:
#  matrixMap:
#    A: [CAAC,     Art, CDP, Arch,   LA,  HP, RUD, SoA]
#    a: [CAH,  

### end ###
