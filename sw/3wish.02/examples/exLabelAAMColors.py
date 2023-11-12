# Code to manually assign colors for chosen YAML-sourced value sequence
# Brygg Ullmer, Clemson University
# Begun 2023-11-11

import yaml
from enoFcTkMidi import *

yfn = 'cuColleges01.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

### end ###
