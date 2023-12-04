# Enodia content support class
# Brygg Ullmer, Clemson University
# Begun 2023-12-04

import traceback
import yaml

################################################################
######################## Enodia Content ########################
################################################################

class enoContent:

  yamlFn    = 'index.yaml'
  yamlD     = None

  countries  = None
  continents = None

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

  ############# getCountries#############

  def getCountries(self):
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

      #except: print("enoContent getCountries glitch, ignoring")
      except: print("enoContent getCountries glitch:", content)

    #return self.countries
    return result

################### main ###################

def main():
  ec = enoContent()

  content = ec.getSection()
  print(len(content))
  print(ec.getCountries())

if __name__ == '__main__': main()

### end ###
