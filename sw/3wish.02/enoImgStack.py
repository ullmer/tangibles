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
        self.setValues3(tcv, [-hx,0,hy], [hx,0,hy], [hx,0,-hy], [-hx,0,-hy])
        tcv.set1Value(0, coin.SbVec3f(-hx, 0, hy)); tcv.set1Value(1, coin.SbVec3f( hx, 0, hy))

  textureName       = None
  textureSize       = None
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

  ############# setValues3 #############

  def setValues3(self, target, values):  #likely migrate to a parent class
    try:
      idx = 0
      for value in values:
        x,y,z=value; target.set1Value(idx, coin.SbVec3f(x,y,z)); idx += 1
    except:
      print("setvalues3 exception:"); traceback.print_exc()
  
  ############# setValues2 #############

  def setValues2(self, target, values):  #likely migrate to a parent class
    try:
      idx = 0
      for value in values:
        x,y=value; target.set1Value(idx, coin.SbVec2f(x,y)); idx += 1
    except:
      print("setvalues2 exception:"); traceback.print_exc()

  ############# assert Iv #############

  def assertTexturePlaneIv(self, textureImgFn, orient='xz'):
    if self.textureName is None: print("enoTexturePlane assertIv: textureName is empty"); return None

    hx, hy = textureSize[0]/2., textureSize[1]/2.

    #see https://github.com/coin3d/pivy/blob/master/examples/Mentor/07.2.TextureCoordinates.py

    match orient:
      self.vertexProperty = coin.SoVertexProperty() 
      tcv = self.vertexProperty.vertex

      case 'xz':
        self.setValues3(tcv, [-hx,0,hy], [hx,0,hy], [hx,0,-hy], [-hx,0,-hy])
        self.vertexProperty.normal.set1Value(0, coin.SbVec3f(0,1,0))

      case 'xy':
        self.setValues3(tcv, [-hx,hy,0], [hx,hy,0], [hx,-hy,0], [-hx,-hy,0])
        self.vertexProperty.normal.set1Value(0, coin.SbVec3f(0,0,1))

    tpn = self.texturedPlaneNode = coin.SoSeparator()
    tc  = self.textureCoord      = coin.TextureCoordinate2()
    self.setValues2(tc, [[1,1], [0,1], [0,0], [1,0])

    t2  = self.texture2 = coin.SoTexture2(); 
    t2.filename.setValue(textureImgFn); t2.model = SoMultiTextureImageElement::DECAL

    nb       = coin.SoNormalBinding()
    nb.value = coin.SoNormalBinding.PER_FACE

    fs = coin.SoFaceSet(); fs.numVertices.setValue(4)

    for e in [tc, t2, nb, n, coords, fs]: tpn.addChild(el)

    IvObj::assertIv

    addNInlineObj $this:transp [format {Material {transparency %s
	 diffuseColor %s}} $transp $color] pre

  }

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

itcl_class texture_stack {

  inherit IvObj

  constructor {config} {
    set members [concat $members $local_members]
  }

  method assertIv {{orient xz}} {
    if {$texture_names == {}} {return} ;#default args don't work
    set imnum 1

    puts "asserting $this"
    addNFrame $this

    foreach texture_name $texture_names {

      set name [format {%s:texture%s} $this $imnum]
      set name_trans [format {%s:trans%s} $this $imnum]

      texture_plane $name -texture_name $texture_name \
	-texture_size $texture_size -color $color

      $name assertIv $orient
      addNInlineObj $name_trans \
	[format {Translation {translation %s}} $img_offset]

      bindNObj $name [format {%s highlight %s} $this $imnum]
      $name changeTransp [lindex $highlights 0]

      incr imnum
    }

    highlight $popout
  }

  method highlight {layer} {
    if {$layer > [llength $texture_names] || $layer < 1}  {return} 
      ;#illegal layer number

    if {$last_highlighted != {}} {
      $last_highlighted changeTransp [lindex $highlights 0]
    }

    set last_highlighted $this:texture$layer
    $last_highlighted changeTransp [lindex $highlights 1]
  }

  public local_members {texture_names texture_size img_offset 
      last_highlighted highlights color popout}

  public texture_names {}
  public texture_size {0 0}
  public img_offset {0 2 0}
  public color {1 1 1}

  public last_highlighted {}
  public highlights {.7 .2}
  public popout {1}
}

