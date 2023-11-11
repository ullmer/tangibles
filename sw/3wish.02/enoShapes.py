# Enodia Shapes
# Brygg Ullmer, Clemson University
# Begun 2023-11-10

import pivy.coin as coin
import traceback

####################### enodia cube ########################

class enoCube:
  diffuseColor   = (1,1,1)
  emmissiveColor = (1,1,1)
  transparency   = 0.7
  size           = (1,1,1)
  node           = None
  materialNode   = None
  cubeNode       = None

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.buildCube()

  ############# get node #############

  def getNode(self): return self.node

  ############# buildCube #############

  def buildTexturePlaneIv(self):
    self.node         = coin.SoSeparator()
    self.materialNode = coin.SoMaterial()
    self.cubeNode     = coin.SoCube()

    self.node.addChild(self.materialNode)
    self.node.addChild(self.cubeNode)

    self.materialNode.diffuseColor  = self.diffuseColor
    self.materialNode.emissiveColor = self.emissiveColor
    self.materialNode.transparency  = self.transparency

### end ###
