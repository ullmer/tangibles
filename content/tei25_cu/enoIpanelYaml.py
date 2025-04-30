# Interaction panel code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, yaml, traceback

############# enodia interaction panel #############

class enoIpanelYaml:

  tagFn = None
  tagYd = None
  tags  = None
  tagCharToCategory = None
  tagCharToCatList  = None
  tagCharToCatLIdx  = None #index within tagCharToCatList keyed arrays

  colorMap  = None
  brightMap = None

  rows, cols       = 8, 8
  verbose          = False

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

      if 'tags' in self.tagYd:
        ytags      = self.tagYd['tags']
        for tag in ytags: self.tags.append(tag)
      else: self.msg('loadYaml: tags not found in ' + str(self.tagFn))
    except: self.err("loadYaml")

  ############# map char to category #############

  def mapCharToCategory(self, tagChar): 
    try:
      if self.verbose: self.msg("mapCharToCategory " + str(tagChar))
      if self.tagCharToCategory is None: self.tagCharToCategory = {}
      if self.tagCharToCatList  is None: self.tagCharToCatList  = {}
      if self.tagCharToCatLIdx  is None: self.tagCharToCatLIdx  = {}

      if tagChar in self.tagCharToCategory: 
        return self.tagCharToCategory[tagChar] #caching important to performance

      try:    cm = self.tagYd['interactionPanel']['charMap']
      except: self.err('mapCharToCategory: problem accessing charMap in YAML descriptor'); return None

      if tagChar not in cm: self.err('mapCharToCategory not finding character ' + str(tagChar)); return None

      cme = cm[tagChar]
      tag = cme[0]

      self.tagCharToCategory[tagChar] = tag
      self.tagCharToCatList[tagChar]  = cme[0:]
      self.tagCharToCatLIdx[tagChar]  = 0

      if self.verbose: self.msg("mapCharToCategory result: " + str(tag))
      return tag
    except: self.err('mapCharToCategory')

  ############# map char to category next element #############

  def mapCharToCatNextEl(self, tagChar): 
    try:
      cat = self.mapCharToCategory(tagChar)
      if tagChar not in self.tagCharToCatList or \
         tagChar not in self.tagCharToCatLIdx:
        #self.err("mapCharToCatNextEl: unexpected condition 0"); return None
        return None

      idx  = self.tagCharToCatLIdx[tagChar]
      catl = self.tagCharToCatList[tagChar]
      clen = len(catl)

      if idx >= clen: return None
        #self.err("mapCharToCatNextEl: unexpected condition 1"); return None

      result = catl[idx]
      self.tagCharToCatLIdx[tagChar] += 1
      return result

    except: self.err('mapCharToCatNextEl')

  ############# getCharMatrix #############

  def getCharMatrix(self):
    try:
      result = self.tagYd['interactionPanel']['charMatrix']
      return result
    except: self.err("getCharMatrix")

  ############# getCharMatrix #############

  def expandMatrixYaml(self):
    result = []
    try:
      m     = self.getCharMatrix()
      mrows = m.splitlines()
      for row in mrows:
        lenrow = len(row.rstrip())
        outrow = []
        for i in range(lenrow):
          ch  = row[i]
          tag = self.mapCharToCatNextEl(ch)
          outrow.append(tag)
        #print(outrow)
        result.append(outrow)
      return result
    except: self.err('expandMatrixYaml')
    return None

############# main #############

if __name__ == "__main__":
  #eip = enoIpanel(tagFn = 'cspan-tags.yaml')
  eipy = enoIpanelYaml(tagFn = 'us-bea.yaml')
  m    = eipy.getCharMatrix()
  print(m)

  #cat1 = eip.mapCharToCategory('p')
  #cat2 = eip.mapCharToCategory('f')
  #print(cat1, cat2)

  my = eipy.expandMatrixYaml()
  print(my)

### end ###
