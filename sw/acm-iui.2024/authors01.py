# Find instances with prior common keywords
# Brygg Ullmer, Clemson University
# Begun 2024-03-16

import sqlite3 # https://docs.python.org/3/library/sqlite3.html
import yaml, traceback

yfn='posters-iui24.yaml'
yf = open(yfn, 'rt')
yd = yaml.safe_load(yf)

p = yd['posters']

## connect to database ##

con   = sqlite3.connect("dl-iui.db3")
cur   = con.cursor()

count2entries = {}

for posterId in p:
  try:
    poster  = p[posterId]
    title   = poster['title']
    authors = ', '.join(poster['authors'])
    elentry = "  %i\t%s\n\t\t" % (posterId, title)

    if 'geo' in poster: 
      geo = poster['geo']
      elentry += "%s: " % (', '.join(geo))

      elentry += authors + "\n"

      entry += elentry
  except: 
    print("missing data on entry %i; ignoring" % posterId)
    print(posterId, p[posterId])
    traceback.print_exc()

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
