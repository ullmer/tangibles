# Enodia Shapes
# Brygg Ullmer, Clemson University
# Begun 2023-11-10

import pivy.coin as coin
import traceback

####################### enodia shape ########################

class enoShape:
  diffuseColor   = (1,1,1)
  emmissiveColor = (1,1,1)
  size           = (1,1,1)
  transparency   = 0.7
  node           = None
  materialNode   = None

  translation     = (0,0,0)
  translationNode = None

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.buildShape()

  ############# get node #############

  def getNode(self): return self.node

  ############# buildShape #############

  def buildShape(self):
    self.node            = coin.SoSeparator()
    self.translationNode = coin.SoTranslation()
    self.materialNode    = coin.SoMaterial()

    self.node.addChild(self.translationNode)
    self.node.addChild(self.materialNode)

    self.translationNode.translation = self.translation

    self.materialNode.diffuseColor   = self.diffuseColor
    self.materialNode.emissiveColor  = self.emissiveColor
    self.materialNode.transparency   = self.transparency

####################### enodia cube ########################

class enoCube(enoShape):
  cubeNode       = None

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.buildShape()

  ############# buildShape #############

  def buildShape(self):
    super(enoCube, self).buildShape()

    self.cubeNode = coin.SoCube()
    self.node.addChild(self.cubeNode)

    w, d, h = self.size
    self.cubeNode.width  = w
    self.cubeNode.height = h
    self.cubeNode.depth  = d

####################### enodia cylinder ########################

class enoCylinder(enoShape):
  cylinderNode       = None

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if len(self.size) > 2: self.size = self.size[0:2] # (e.g.) 3-part dimensionality would cause issues
    self.buildShape()

  ############# buildShape #############

  def buildShape(self):
    super(enoCylinder, self).buildShape()

    self.cylinderNode = coin.SoCylinder()
    self.node.addChild(self.cylinderNode)

    r, h = self.size
    self.cylinderNode.radius = r
    self.cylinderNode.height = h

### end ###

