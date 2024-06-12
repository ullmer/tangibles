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
print("num people:", numPeople)

listFields = ['geo', 'bks', 'edu', 'orgs']

categoryDictCounts    = {} # a dictionary of dictionaries, counts of categories
categoryDictNameLists = {} # a dictionary of dictionaries, names within categories
categoryDictDataLists = {} # a dictionary of dictionaries, data structurs w/in categories

for field in listFields:
  categoryDictCounts[field]    = {}
  categoryDictNameLists[field] = {}
  categoryDictDataLists[field] = {}

categoryCounts = {}

for personData in yd:
  fields = personData.keys()
  for field in fields: 
    if field in categoryCounts: categoryCounts[field] += 1
    else:                       categoryCounts[field]  = 1

    if field in categoryDictCounts:
      cdc  = categoryDictCounts[field]
      cdnl = categoryDictNameLists[field]
      cddl = categoryDictDataLists[field]
      vals = personData[field]

      for val in vals:
        if    'n' in personData: name = ' '.join(personData['n'])  #name field, not always present
        elif 'nn' in personData: name = personData['nn'] #nickname/abbrev, not always present
        else:                    name = 'unknown'

        if val in cdnl: cdnl[val].append(name); cddl[val].append(personData)
        else:           cdnl[val] = [name];     cddl[val] = [personData]

print("fields observed")
for field in categoryCounts:
  numObserved = categoryCounts[field]
  print("field %s; \t num observed: %i" % (field, numObserved))

#print(categoryDictCounts)

print("Individuals associated with Massachusetts:", categoryDictNameLists['geo']['MA'])

maPeopleData = categoryDictDataLists['geo']['MA']
bookList = []

for maPeople in maPeopleData:
  if 'bk' in maPeople: bookList += maPeople['bk']

print("\nBooks associated with people associated with Massachusetts:", bookList)

### end ###
