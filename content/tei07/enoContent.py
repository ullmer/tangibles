# Enodia content support class
# Brygg Ullmer, Clemson University
# Begun 2023-12-04

import yaml

################################################################
######################## Enodia Content ########################
################################################################

class enoContent:

  yamlFn   = 'index.yaml'
  yamlD    = None
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

    #print(self.yamlD)

  ############# getSection #############

  def getSection(self, whichSection=None):
    if whichSection is None:       whichSection = self.sections[0]
    if whichSection in self.yamlD: return self.yamlD[whichSection]
    return None

################### main ###################

def main():
  ec = enoContent()

if __name__ == '__main__': main()

### end ###
