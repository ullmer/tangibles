# Sqlite3 ACM helper functions for populating YAML
# By Brygg Ullmer, Clemson University
# Begun 2024-03-18

import yaml
import sqlite3 # https://docs.python.org/3/library/sqlite3.html

dbfn = 'dl-iui.db3'
yfn  = 'posters-iui24.yaml'
numPosters = 34

con  = sqlite3.connect(dbfn)
cur  = con.cursor()

yf   = open(yfn, 'rt')
yd   = yaml.safe_load(yf)

posters = yd['posters']
print("P:", posters)
for i in range(1,numPosters+1):
  p = posters[i]
  t = p['title']
  print(i, t)

#titleIds  = [781, 1031, 1560, 1751, 2073, 2084, 2189]
#ti  = str(titleIds)[1:-1]
#
#query = """select k.id, k.keyword from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where
#             t.id in (%s)
#             and ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;""" % (ti)
#print(query)
#
#result  = cur.execute(query)
#qresult = result.fetchall()
#
#kwIds   = []
#kwNames = []
#
#for el in qresult:
#  id, name = el
#  kwIds.append(id)
#  kwNames.append(name)
#
#kwIds.sort()
#kwNames.sort()
#kwn = ', '.join(kwNames)
#
#print('priorKwIds:',   kwIds)
#print('priorKwNames: [' +  kwn + ']')
#
### end ###
