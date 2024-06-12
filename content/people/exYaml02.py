# A few engagements with the provided example YAML description of 
# an eclectic selection of people, potentially jointly supportive
# of some public library deployments and experimentations in the 
# Animist project community
# Brygg Ullmer, Clemson University
# Begun 2024-06-12

import yaml, traceback

yfn = 'people01.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)


numPeople = len(yd)

### end ###
