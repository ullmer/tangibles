# 3Wish Python port
# By Brygg Ullmer (orig version @MIT Media Lab, port @Clemson University)
# Originally disaggregated from tcl_examp3 1995-11-24
# Python port begun 2023-10-20

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import traceback

global HIERSEP_CHAR 
HIERSEP_CHAR = ':'

################ gen view sg root ################ 

def genViewDocSgRoot(): 

  if Gui.ActiveDocument is None:
    doc  = App.newDocument()
    #doc.recompute()
    viewer = Gui.createViewer()
    view   = viewer.getViewer()
  else:
    doc  = Gui.ActiveDocument
    view = Gui.ActiveDocument.ActiveView

  Gui.activeDocument().activeView().setCameraType("Perspective")

  sg      = view.getSceneGraph()
  root    = coin.SoSeparator()
  sg.addChild(root)

  result = [view, doc, sg, root]
  return result

################ Add Obj ################ 
# Initially, push passed text Iv Obj onto space

def addObj(parent, obj):
   try:
     parent.addChild(obj)
   except:
     print("addObj exception:"); traceback.print_exc()
     return False

   return True

################ Get camera, node fields ################ 

#The above two code excerpts are from here:
#https://forum.freecad.org/viewtopic.php?f=22&t=13198

def getCamera():
  cam=Gui.ActiveDocument.ActiveView.getCameraNode()
  return cam

def getNodeFields(node):
  d=node.getFieldData()
  result = []
  for iField in range(0,d.getNumFields()):
    result.append(d.getFieldName(iField))
  return result

################ Get camera configuration ################ 

def getCameraConfig():
  cfields = "viewportMapping position orientation nearDistance farDistance aspectRatio focalDistance heightAngle".split(' ')
  cdict   = {}
  cam     = getCamera()
  for cfield in cfields:
    fieldObj = cam.getField(cfield)
    fieldVal = fieldObj.getValue() 
    if isinstance(fieldVal, coin.SbVec3f) or isinstance(fieldVal, coin.SbRotation): #one more level of indirection necessary
      fieldVal = fieldVal.getValue()
    cdict[cfield] = fieldVal

  return cdict

#camera: {viewportMapping: 3,  position: [28.4, 12.3,  12.8], focalDistance: 31.1, heightAngle: 0.785,
#         aspectRatio: 1.0, orientation: [0.335, 0.316, 0.628, 0.627], nearDistance: 2.1, farDistance: 33.6}

#camera: {'viewportMapping': 3,  'position': [28.4, 12.3,  12.8], 'focalDistance': 31.1, 'heightAngle': 0.785,
#         'aspectRatio': 1.0, 'orientation': [0.335, 0.316, 0.628, 0.627], 'nearDistance': 2.1, 'farDistance': 33.6}

################ set camera configuration ################ 

def setCameraConfig(cameraDict):
  try:
    cam = getCamera()
    for cfield in cameraDict:
      val      = cameraDict[cfield]
      fieldObj = cam.getField(cfield)
      fieldObj.setValue(val)
  except:
    print("setCameraConfig exception:"); traceback.print_exc(); return None

################ Get Named  Node ################ 

def getNamedNode(parent, name):
  search = coin.SoSearchAction()
  search.setName(name)
  search.apply(parent)
  path = search.getPath()
 
  if path is None: return None

  return path.getTail()

################ Get Named Node Path ################ 

def getNamedNodePath(parent, name):
  search = coin.SoSearchAction()
  search.setName(name)
  search.apply(parent)
  path = search.getPath()

  if path is None: return None
  return path

################ Add Named Inline Obj   ################ 
# Push single text Iv Obj inline into parent (instead of inside own sep)
# addNInlineObj name iv

def addNInlineObj(parent, name, obj, prepend=True):
  try:
    sep = getObjSeparator(parent, name)

    if sep is None:
      print("addNInlineObj error: \"%s\" does not have a valid parent frame!" % name)
      return False

    if prepend: sep.insertChild(obj, 0)
    else:       sep.addChild(obj)

    return True
  except:
    print("addNFrame exception:"); traceback.print_exc()
    return False

################ Add Named Obj ################ 
# Push passed text Iv Obj onto space as a named object
# addNObj name iv

def addNObj(root, name, obj, prepend=False): #default is to append
  obj.setName(name)
  parent = getParentFrame(root, name);

  if parent is None:
    print("addNFrame error: %s does not have a valid parent frame!" % name)
    return False

  if prepend: parent.insertChild(newNode, 0)
  else:       parent.addChild(obj)

  return True

################ Add Named Frame ################ 
# Adds a named separator.  Introduces support for hierarchy
# addNFrame name 

def addNFrame(parent, name):
  try:
    sep = coin.SoSeparator()
    sep.ref()
    sep.setName(name)
    parent.addChild(sep)
    sep.unref()

    return True
  except:
    print("addNFrame exception:"); traceback.print_exc()
    return False

################ Deleted Named Obj ################ 

def delNObj(root, name):
   try:
     search = coin.SoSearchAction()
     search.setName(name)
     search.apply(root)
     path = search.getPath();

     if path is None:
       print("delNObj error: can't find \"%s\"!" % name);
       return False
 
     parent = path.getNodeFromTail(1);
     if parent is None:
       print("delNObj error: issue extracting \"%s\"!" % name);
       return False

     if parent.isOfType(coin.SoSeparator.getClassTypeId()):
        #we've got a valid parent
        parent.removeChild(path.getTail())
        return True
     else: 
        print("delNObj: problem with removing child %s!" % name);
        return False

   except:
     print("addObj exception:"); traceback.print_exc()
     return False

################ Tweak Named Obj ################ 
### Get Inventor scene graph contents associated with a name

def tweakNObj(root, name, params):
   node = getNamedNode(root, name)

   if node is None:
     print("tweakNObj error: can't find \"%s\"!" % name)
     return False
   
   result = setParams(node, params) #needs iteration
   return result

################ Get Named Obj ################ 
# Get Inventor scene graph contents associated with a name

def getNObj(root, name):
  node = getNamedNode(root, name)
  return node

################ Get Named Obj ################ 
# Get Inventor scene graph contents associated with a name

def writeObj(node, fn):
  out = coin.SoOutput()
  out.openFile(fn) #output.setBuffer( #still deciphering SWIG mapping
  wa = coin.SoWriteAction(out)
  wa.apply(node)
  wa.getOutput().closeFile()
  #out.close()

################# Get Parent Frame ################ 
## Used by addNFrame and addNObj to get parent node

def getParentFrame(root, name): 
  global HIERSEP_CHAR 

  try:
    idx=name.rfind(HIERSEP_CHAR)
    if idx == -1: # we have a root frame
      return root

    #Find node handle to parent node  
    parentname = name[:idx]
    parentNode = getNamedNode(root, parentname)

    if parentNode is None:
      print("getObjSeparator error: can't find \"%s\"!" % name)
      return None

    if not node.isOfType(coin.SoGroup.getClassTypeId()): #"parent" is not a Separator
      print("getParentFrame error: parent frame \"%s\" is not a Separator!" % parentname);
      return None

    return parentNode

  except:
    print("getObjSeparator exception:"); traceback.print_exc()
    return False

################# Get named object transformation ################ 
## Borrowing again from 1995 3wish cod

def getNObjTransf(root, node, viewport):
  matrixAction = coin.SoGetMatrixAction(viewport) 
  search       = coin.SoSearchAction()
  search.setName(name)
  search.apply(parent)
  path = search.getPath()


  path         = getNamedNodePath(node)
  matrixAction.apply(node)

  matrix       = matrixAction.getMatrix()
  matrix.getTransform(translation, rotation, scale, scaleorient)

  result = []
  for i in range(3): result.append(translation[i])
  return result

### end ###

