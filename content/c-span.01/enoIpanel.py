# Interaction panel code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback

############# enodia interaction panel #############

class enoIpanel:

  tagFn = None
  tagYd = None
  tags  = None
  tagCharToCategory = None

  rows, cols       = 8, 8
  verbose          = True

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.tagFn is not None: self.loadYaml()

  ############# error, msg #############

  def err(self, msg): print("enoIpanel error: " + str(msg)); traceback.print_exc(); 
  def msg(self, msg): print("enoIpanel msg: "   + str(msg))

  ############# load yaml #############

  def loadYaml(self):
    self.tags  = []

    try:
      yf         = open(self.tagFn, 'rt')
      self.tagYd = yaml.safe_load(yf)

      ytags      = self.tagYd['tags']
      for tag in ytags: self.tags.append(tag)
    except: self.err("loadYaml")

  ############# map char to category #############

  def mapCharToCategory(self, tagChar): 
    try:
      if self.verbose: self.msg("mapCharToCategory " + str(tagChar))
      if self.tagCharToCategory is None: self.tagCharToCategory = {}

      if tagChar in self.tagCharToCategory: 
        return self.tagCharToCategory[tagChar] #caching important to performance

      try:    cm = self.tagYd['interactionPanel']['charMap']
      except: self.err('mapCharToColor: problem accessing charMap in YAML descriptor'); return None

      if tagChar not in cm: self.err('mapCharToColor not finding character ' + str(tagChar)); return None

      cme = cm[tagChar]
      tag = cme[0]

      if self.verbose: self.msg("mapCharToColor : tag " + str(tag))

      dcl = self.getDeviceColorLookup(self.midiCtrlName)

      if self.verbose: self.msg("mapCharToColor: dcl: " + str(dcl))

      if tag not in dcl: 
        self.err("mapCharToColor: device color lookup " + str(dcl) + " not found in yaml " + self.tagFn)
        return None

      color = dcl[tag]
      if self.verbose: self.msg("mapCharToColor result: " + str(color))

  ############# getCharMatrix #############

  def getCharMatrix(self):
    try:
      result = self.tagYd['interactionPanel']['charMatrix']
      return result
    except: self.err("getCharMatrix")

############# main #############

if __name__ == "__main__":
  cm = enoIpanel(tagFn = 'cspan-tags.yaml')
  m  = cm.getCharMatrix()
  print(m)

### end ###
