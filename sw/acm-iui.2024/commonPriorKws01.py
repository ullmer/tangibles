# Find instances with prior common keywords
# Brygg Ullmer, Clemson University
# Begun 2024-03-16

import yaml

yfn='posters-iui24.yaml'
yf = open(yfn, 'rt')
yd = yaml.safe_load(yf)

p = yd['posters']

keywordId2papers = {}
for key in p: # iterate through papers
  el = p[key]
  if 'priorKwIds' in el:
    priorKwIds = el['priorKwIds']
    for kwId in priorKwIds:
      if kwId not in keywordId2papers: keywordId2papers[kwId] = []
      keywordId2papers[kwId].append(key)

## search for commonalities ##

for key in keywordId2papers:
  val = keywordId2papers[key]
  if len(val) > 1: print(key, val)

### end ###
