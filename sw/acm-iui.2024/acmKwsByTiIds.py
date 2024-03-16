# Sqlite3 ACM helper functions for populating YAML
# By Brygg Ullmer, Clemson University
# Begun 2024-03-15

import sqlite3 # https://docs.python.org/3/library/sqlite3.html

con   = sqlite3.connect("dl-iui.db3")
cur   = con.cursor()
query = """select k.id, k.keyword from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where
             t.id in (367, 471, 474, 792, 969, 1308, 1327, 1480, 2113, 2185, 2268)
             and ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;"""

result  = cur.execute(query)
qresult = result.fetchall()

kwIds   = []
kwNames = []

for el in qresult:
  id, name = el
  kwIds.append(id)
  kwNames.append(name)

kwIds.sort()
kwNames.sort()
kwn = ', '.join(kwNames)

print('priorKwIds:',   kwIds)
print('priorKwNames: [' +  kwn + ']')

### end ###
