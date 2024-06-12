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

categoryDicts = { # a dictionary of dictionaries, lookups for list fields
   'geo':  {}, 
   'bks':  {},
   'edu':  {}, 
   'orgs': {}}

categoryCounts = {}

for personData in yd:
  fields = personData.keys()
  for field in fields: 
    if field in categoryCounts: categoryCounts[field] += 1
    else:                       categoryCounts[field]  = 1
    if field in 

print("fields observed")
for field in categoryCounts:
  numObserved = categoryCounts[field]
  print("field %s; \t num observed: %i" % (field, numObserved))

### end ###
