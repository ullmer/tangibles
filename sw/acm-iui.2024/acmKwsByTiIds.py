# Sqlite3 ACM helper functions for populating YAML
# By Brygg Ullmer, Clemson University
# Begun 2024-03-15

import sqlite3 # https://docs.python.org/3/library/sqlite3.html

#titleIds = [443, 644, 868, 1076, 1286, 1402, 1591, 1605, 2280]
#titleIds = [423, 1320, 1578, 2056]
#titleIds = [108, 1295, 1509, 2007, 2216, 2303]
#titleIds = [911, 944, 973, 1537, 2025, 2035]
#titleIds = [954]
#titleIds = [944, 1738]
#titleIds  = [1339, 1459, 1617, 2161]
#titleIds  = [2159]
#titleIds  = [841, 1242, 1338, 1524]
titleIds  = [781, 1031, 1560, 1751, 2073, 2084, 2189]

ti  = str(titleIds)[1:-1]

con   = sqlite3.connect("dl-iui.db3")
cur   = con.cursor()
query = """select k.id, k.keyword from titles as t, keywords as k, ti_kw as tk, ti_au as ta, authors as a where
             t.id in (%s)
             and ta.ti_id = t.id and ta.au_id = a.id and tk.ti_id = t.id and tk.kw_id = k.id group by keyword;""" % (ti)
print(query)

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
