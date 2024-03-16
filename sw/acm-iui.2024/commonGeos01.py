# Find instances with prior common keywords
# Brygg Ullmer, Clemson University
# Begun 2024-03-16

import yaml

yfn='posters-iui24.yaml'
yf = open(yfn, 'rt')
yd = yaml.safe_load(yf)

p = yd['posters']

geo2papers = {}

for key in p: # iterate through papers
  el = p[key]
  if 'geo' in el:
    geo = el['geo']
    for g in geo:
      if g not in geo2papers: geo2papers[g] = []
      geo2papers[g].append(key)

## search for commonalities ##

for key in geo2papers:
  val = geo2papers[key]
  if len(val) > 1: print(key, val)

### end ###
