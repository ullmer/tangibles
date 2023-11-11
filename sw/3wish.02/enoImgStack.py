# Stack of Image objects
# Brygg Ullmer: initially MIT Media Lab VLW/TMG, presently Clemson University
# Originally written March 4, 1996
# Python port begun 2023-11-02

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import traceback

########################## Texture Plane ###########################

class enoTexturePlane:
  translationVal    = None
  translationNode   = None
  textureImgFn      = None
  textureSize       = (1,1)
  textureCoord      = None
  vertexProperty    = None
  texturedPlaneNode = None
  transparencyMaterialNode  = None

  diffuseColor = (1,1,1)
  transparency = 0.7

  ############# constructor #############

  def __init__(self, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if self.textureImgFn is not None:
      self.buildTexturePlaneIv()

  ############# setValues3 #############

  def setValues3(self, target, values):  #likely migrate to a parent class
    try:
      idx = 0
      for value in values:
        x,y,z=value; target.set1Value(idx, coin.SbVec3f(x,y,z)); idx += 1
    except:
      print("setValues3 exception:"); traceback.print_exc()
  
  ############# setValues2 #############

  def setValues2(self, target, values):  #likely migrate to a parent class
    try:
      idx = 0
      for value in values:
        x,y=value; target.set1Value(idx, coin.SbVec2f(x,y)); idx += 1
    except:
      print("setValues2 exception:"); traceback.print_exc()

  ############# assert Iv #############

  def getNode(self):
    result = self.texturedPlaneNode 
    return result

  ############# assert Iv #############

  def buildTexturePlaneIv(self, orient='xz'):
    if self.textureImgFn is None: print("enoTexturePlane assertIv: textureImgFn is empty"); return None

    hx, hy = self.textureSize[0]/2., self.textureSize[1]/2.

    #see https://github.com/coin3d/pivy/blob/master/examples/Mentor/07.2.TextureCoordinates.py
    #self.vertexProperty = coin.SoVertexProperty() 

    c3 = coin.SoCoordinate3()
    n  = coin.SoNormal()
    #tcv = self.vertexProperty.vertex

    if orient == 'xz':
      self.setValues3(c3.point, [[-hx,0,hy], [hx,0,hy], [hx,0,-hy], [-hx,0,-hy]])
      self.setValues3(n, [[0,1,0]])

    if orient == 'xy':
      self.setValues3(c3.point, [[-hx,hy,0], [hx,hy,0], [hx,-hy,0], [-hx,-hy,0]])
      self.setValues3(n, [[0,0,1]])

    tpn = self.texturedPlaneNode = coin.SoSeparator()

    if self.translationVal is not None:
      self.translationNode = coin.SoTranslation()
      self.translationNode.translation = self.translationVal
      tpn.addChild(self.translationNode)

    tc  = self.textureCoord      = coin.SoTextureCoordinate2()
    self.setValues2(tc.point, [[1,1], [0,1], [0,0], [1,0]])

    t2  = self.texture2 = coin.SoTexture2(); 
    t2.filename.setValue(self.textureImgFn)
    t2.model = coin.SoMultiTextureImageElement.DECAL

    nb       = coin.SoNormalBinding()
    nb.value = coin.SoNormalBinding.PER_FACE

    fs = coin.SoFaceSet(); fs.numVertices.setValue(4)

    for el in [tc, t2, nb, n, c3, fs]: tpn.addChild(el)
    return tpn

  ############# change transparency #############

  def changeTransp(self, newVal):
    if self.texturePlaneNode is None:
      print("enoImgStack changeTransp error: texturePlaneNode unassigned"); return None

    if self.transparencyMaterialNode is None:
      m = coin.SoMaterial()
      m.transparency = self.transparency = newVal
      m.diffuseColor = self.diffuseColor
      self.transparencyMaterialNode = m
      self.texturePlaneNode.insertChild(m, 0) #prepend 
    else: 
      self.transparencyMaterialNode.transparency = newVal
      self.transparency = newVal

########################## Texture Stack ###########################

class enoTextureStack:

  textureImgFns  = None
  textureSize   = [0,0]
  img_offset    = [0,2,0]
  diffuseColor  = (1,1,1)
  lastHighlight = None
  highlights    = [.7, .2]
  popout        = 1


#  method assertIv {{orient xz}} {
#    if {$texture_names == {}} {return} ;#default args don't work
#    set imnum 1
#
#    puts "asserting $this"
#    addNFrame $this
#
#    foreach texture_name $texture_names {
#
#      set name [format {%s:texture%s} $this $imnum]
#      set name_trans [format {%s:trans%s} $this $imnum]
#
#      texture_plane $name -texture_name $texture_name \
#	-texture_size $texture_size -color $color
#
#      $name assertIv $orient
#      addNInlineObj $name_trans \
#	[format {Translation {translation %s}} $img_offset]
#
#      bindNObj $name [format {%s highlight %s} $this $imnum]
#      $name changeTransp [lindex $highlights 0]
#
#      incr imnum
#    }
#
#    highlight $popout
#  }
#
#  def highlight(self, whichLayer):
#    tnLen = length(self.textureImgFns)
#    if whichLayer > tnLen or whichLayer < 1:
#      print("enoImgStack enoTextureStack highlight error: bad layer specifier %i (%i)" % (whichLayer, tnLen)); return None
# 
#    if self.lastHighlighted is not None: self.lastHighlighted.changeTransp(
#
#    else:
#     self.lastHighlighted = 
#  
#
#    if {$last_highlighted != {}} {
#      $last_highlighted changeTransp [lindex $highlights 0]
#    }
#
#    set last_highlighted $this:texture$layer
#    $last_highlighted changeTransp [lindex $highlights 1]
#  }
#
#### end ###
