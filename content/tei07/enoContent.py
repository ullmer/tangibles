# Enodia content support class
# Brygg Ullmer, Clemson University
# Begun 2023-12-04

import traceback
import yaml

################################################################
######################## Enodia Content ########################
################################################################

class enoContent:

  yamlFn     = 'index.yaml'
  yamlD      = None

  countries     = None
  continents    = None
  themesYaml    = None
  themesPapers  = None
  keywordCounts = None
  keywordPapers = None

  country2continentAbbrev = None

  primaryC = 'content' #name would benefit from evolution
  sections = ['contributions']

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.yamlFn is not None: self.loadYaml()

  ############# load YAML #############

  def loadYaml(self):
    if self.yamlFn is None:
      print('enoContent loadYaml: yamlFn is None'); return None

    yf         = open(self.yamlFn, 'rt')
    self.yamlD = yaml.safe_load(yf)

    self.populateContinentMappings()

    #print(self.yamlD)

  ############# getSection #############

  def getSection(self, whichSection=None):
    if whichSection is None:       whichSection = self.sections[0]
    pc = self.primaryC
   
    if pc not in self.yamlD: return None

    if whichSection in self.yamlD[pc]: return self.yamlD[pc][whichSection]
    return None

  ############# populateContinentMappings #############

  def populateContinentMappings(self):
    pc = self.primaryC
    if 'continents' in self.yamlD[pc]: self.continents = self.yamlD[pc]['continents']

    self.country2continentAbbrev = {}
    #print("continents:", self.continents)

    for continent in self.continents:
      try:
        abbrev    = self.continents[continent]['abbrev']
        instances = self.continents[continent]['instances']
        for country in instances:
          self.country2continentAbbrev[country] = abbrev
      except: print("enoContent populateContinentMappings: error on", continent); traceback.print_exc()

    #print(self.country2continentAbbrev)

  ############# country 2 continentAbbrev #############
  
  def getCountryContinentAbbrev(self, country):
  
    if self.country2continentAbbrev is None:        print("enoContent getCountryContinentAbbrev: c2cA not populated"); return None
    if country not in self.country2continentAbbrev: print("enoContent getCountryContinentAbbrev: country not in c2cA", country); return None

    result = self.country2continentAbbrev[country]
    return result

  ############# collapse country continent abbreviations #############
  
  def collapseCountryContinentAbbrev(self, countryList):
    continentAbbrevs = {}
    result           = ""

    for country in countryList: 
      continentAbbrev = self.getCountryContinentAbbrev(country)
      continentAbbrevs[continentAbbrev] = True

    for continentAbbrev in continentAbbrevs: result += continentAbbrev
    return result


  ############# tallyCountries#############

  def tallyCountries(self):
    self.countries = {}
    mainSection    = self.getSection()
    result         = {}
  
    for content in mainSection:
      try:
        authors   = mainSection[content]['authors']
        countries = []
        for author in authors:
          country = author[-1]
          countries.append(country)
          if country not in self.countries: self.countries[country]  = 1
          else:                             self.countries[country] += 1 

        #result.append(countries)
        cca = self.collapseCountryContinentAbbrev(countries)

        if cca in result: result[cca] += 1
        else            : result[cca]  = 1

      #except: print("enoContent tallyCountries glitch, ignoring")
      except: print("enoContent tallyCountries glitch:", content)

    #return self.countries
    return result

  ############# tallyKeywords #############

  def tallyKeywords(self):
    mainSection    = self.getSection()

    self.keywordCounts = {}
    self.keywordPapers = {}

    for content in mainSection:
      try:
        if 'keywords' in mainSection[content]:
          keywords = mainSection[content]['keywords']
          for kw in keywords:
            if kw not in self.keywordCounts: self.keywordCounts[kw]  = 1; self.keywordPapers[kw] = [content]
            else:                            self.keywordCounts[kw] += 1; self.keywordPapers[kw].append(content)

      except: print("enoContent tallyKeywords glitch:", content); traceback.print_exc()

  ############# tallyThemes #############

  def tallyThemes(self):
    self.themesYaml   = self.getSection('themes')
    self.themesPapers = {}

    for theme in self.themesYaml:
      papers = {}
      try:
        if 'kw' in theme:
          kws = theme['kw']
          for kw in kws:
            if kw in self.keywordPapers: 
              kwpapers = self.keywordPapers[kw]
              for paper in kwpapers: papers[paper] = True
        self.themesPapers[themes] = papers

      except: print("enoContent tallyThemes glitch:", theme); traceback.print_exc()

    return self.themesPapers

################### main ###################

def main():
  ec = enoContent()

  content = ec.getSection()
  print(len(content))
  c      = ec.tallyCountries()
  kwDict = ec.tallyKeywords()
  thPap  = ec.tallyThemes()

  kws = []
  for keyword in kwDict:
    count = kwDict[keyword]
    kws.append("%s: %i" % (keyword, count))

  kws.sort()

  #for el in kws:
  #  print(el)

  for theme in thPap:
    papers = thPap[theme]
    pcount = len(papers)
    print("%s: %i (%s)" % (theme, pcount, papers))

if __name__ == '__main__': main()

### end ###
