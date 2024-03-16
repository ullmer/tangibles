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

count2entries = {}

## search for commonalities ##

for key in keywordId2papers:
  val   = keywordId2papers[key]
  count = len(val)
  if count > 1: 

    query = 'select keyword from keywords where id=%i;' % key
    result  = cur.execute(query)
    qresult = result.fetchone()
   
    #entry = str(key) + str(val) + str(qresult[0])
    keyword = qresult[0]
    entry = keyword + "\n"
    for posterId in val:
      try:
        poster  = p[posterId]
        title   = poster['title']
        authors = ', '.join(poster['authors'])
        elentry = "  %i\t%s\t(%s)\n" % (posterId, title, authors)
        entry += elentry
      except: 
        print("missing data on entry %i; ignoring" % posterId)
        print(posterId, p[posterId])

    if count not in count2entries: count2entries[count] = []
    count2entries[count].append(entry)

counts = list(count2entries.keys())
counts.sort(reverse=True)
#print(counts)

for count in counts:
  hashbar = '=' * 15
  print("\n%s %i %s" % (hashbar, count, hashbar)) 
  els = count2entries[count]
  for el in els: print(el)

### end ###
