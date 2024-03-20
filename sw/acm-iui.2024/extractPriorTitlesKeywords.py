# Sqlite3 ACM helper functions for populating YAML
# By Brygg Ullmer, Clemson University
# Begun 2024-03-18

import yaml
import traceback
import sqlite3 # https://docs.python.org/3/library/sqlite3.html

dbfn = 'dl-iui.db3'
yfn  = 'posters-iui24.yaml'
numPosters = 34

con  = sqlite3.connect(dbfn)
cur  = con.cursor()

yf   = open(yfn, 'rt')
yd   = yaml.safe_load(yf)

posters = yd['posters']
for i in range(1,numPosters+1):
  p = posters[i]
  t = p['title']
  print(str(i) + ':')
  print('  title: "%s"' % t)

  try:
    key = 'priorPaperIds'
    if key in p: 
      priorPID = p[key]
      priorPIDstr = []
      for el in priorPID: priorPIDstr.append(str(el))
      pp=','.join(priorPIDstr)
      print("P", priorPID)
      query = "select year, title from titles where t.id in (%s); " % pp
      print(query)

      result  = cur.execute(query)
      qresult = result.fetchall()
      for year, title in qresult: print('    - {year: %s, title: "%s"}' % (year, title))
  except: traceback.print_exc()

  try:
    key = 'priorKwIds'
    if key in p: 
      priorPID = p[key]
      priorPIDstr = []
      for el in priorPID: priorPIDstr.append(str(el))
      pp=','.join(priorPIDstr)
      print("K", priorPID)
      query = """select k.keyword, k.count from titles as t, keywords as k, ti_kw as tk where
                   t.id in (%s)
                  and ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;""" % (pp)
      print(query)

      result  = cur.execute(query)
      qresult = result.fetchall()
      for el in qresult: print(el)

  except: traceback.print_exc()

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
