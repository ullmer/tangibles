# Scene support routines, initially for FreeCAD
# Brygg Ullmer, Clemson University
# Original code begun fall 1995; here, 2023-10-20

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import pyyaml

################# Enodia FreeCAD Add Object ################# 

def enoFcParseYaml(doc, yamlFn):

################# Enodia FreeCAD Add Object ################# 

def enoFcAddObjectY(doc, yamlDescr):


#Heider & Simmel 1944 variant; https://www.youtube.com/watch?v=VTNmLt7QX8E
stage  = doc.addObject("Part::Plane", "floor")  #https://wiki.freecad.org/Part_Plane
bldg1a = doc.addObject("Part::Box",   "bldg1a")
bldg1b = doc.addObject("Part::Box",   "bldg1b")

screen1 = doc.addObject("Part::Plane", "screen1") 
screen2 = doc.addObject("Part::Plane", "screen2") 

stage.Length     = stage.Width  = 32.
bldg1a.Length    = bldg1a.Width = 28.; bldg1a.Height = 3.
bldg1b.Length    = bldg1b.Width = 26.; bldg1b.Height = 3.
screen1.Width    = 8
screen1.Length   = 8. / 1.77 # 1920/1080 ~= 1.77
screen2.Width    = screen1.Width
screen2.Length   = screen1.Length

stage.Placement   = App.Placement(App.Vector(-1,   -1, 0), App.Rotation( 0, 0, 0))
bldg1a.Placement  = App.Placement(App.Vector( 0,    0, 0), App.Rotation( 0, 0, 0))
bldg1b.Placement  = App.Placement(App.Vector( 1,    1, 1), App.Rotation( 0, 0, 0))
screen1.Placement = App.Placement(App.Vector( 3,    3, 5), App.Rotation( 0, 90, 0))
screen2.Placement = App.Placement(App.Vector( 11.5, 3, 5), App.Rotation( 0, 90, 0))

bldgCut1   = App.activeDocument().addObject("Part::Cut", "Bldg central void")
bldgCut1.Base = bldg1a
bldgCut1.Tool = bldg1b

doc.recompute()

Gui.runCommand('Std_ViewZoomOut',0)
Gui.SendMsgToActiveView("ViewFit")

pygame.midi.init()

############ update midi ############

def updateMidi(arg1, arg2):
  global midiIn
  e = midiIn.read(100); 
  if len(e) > 2: 
     events = e[1:]
     #print(e)
     print(len(events), events)
     #for event in e[1]
 

global midiIn
midiIn = pygame.midi.Input(1)

e = midiIn.read(100); print(e)

ts = coin.SoTimerSensor(updateMidi, 0)
ts.schedule()

### end ###
### Example scene (initially, for FreeCAD engagement)
# Brygg Ullmer, Clemson University
# Begun 2023-11-01

scene:
 - {name: bldg1a,  type: box,   dimensions: [28, 28, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
 - {name: bldg1b,  type: box,   dimensions: [26, 26, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
 - {name: floor,   type: plane, dimensions: [32, 32],    placement: [[-1, -1,   0], [0,  0, 0]]}
 - {name: screen1, type: plane, dimensions: [ 8,  4.5],  placement: [[ 3,  3,   5], [0, 90, 0]]}
 - {name: screen2, type: plane, dimensions: [ 8,  4.5],  placement: [[ 3, 11.5, 5], [0, 90, 0]]}

booleanOps:
 - {name: bldgCut1, op: cut, descr: building central void, base: bldg1a, tool: bldg1b}

### end ###

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

################ Get Named  Node ################ 

def getNamedNode(parent, name):
  search = coin.SoSearchAction()
  search.setName(name)
  search.apply(parent)
  path = search.getPath()
 
  if path is None: return None

  return path.getTail()

################ Get Named Node Path ################ 

def getNamedNodePath (parent, name):
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

### end ###

