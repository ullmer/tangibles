# Find instances with prior common keywords
# Brygg Ullmer, Clemson University
# Begun 2024-03-16

import sqlite3 # https://docs.python.org/3/library/sqlite3.html
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

## connect to database ##

con   = sqlite3.connect("dl-iui.db3")
cur   = con.cursor()

## search for commonalities ##

for key in keywordId2papers:
  val = keywordId2papers[key]
  if len(val) > 1: 

    query = 'select keyword from keywords where id=%i;' % key
    result  = cur.execute(query)
    qresult = result.fetchone()
    print(key, val, qresult)

### end ###
