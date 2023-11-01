# Scene support routines, initially for FreeCAD
# Brygg Ullmer, Clemson University
# Original code begun fall 1995; here, 2023-10-20

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import yaml

#####################  Enodia 
##################### 

class enoFreecad:
  yamlFn    = None
  yamlD     = None
  yamlScene = None

  fcObjHandles = {}

  ############# constructor #############

  def __init__(self, yamlFn=None, **kwargs):
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    if yamlFn is not None: self.loadYaml(yamlFn)

  ################# Add Object ################# 

  def parseYaml(self, yamlFn):
    try:
      self.yamlFn = yamlFn
      f           = open(yamlFn, 'rt')
      self.yamlD  = yaml.safe_load(f)

      if 'scene' in self.yamlD:
        self.yamlScene = self.yamlD['scene']
        if not isinstance(self.yamlScene, list):
           print("enoFreecad parseYaml error: scene found, but does not contain a list"); return None
        
        for el in self.yamlScene: self.addObjectY(el)
    except:
      print("enoFreecad parseYaml exception:"); traceback.print_exc(); return None

  ################# Add Object by parsed YAML description ################# 

  def addObjectY(self, objY):

 #- {name: bldg1a,  type: box,   dimensions: [28, 28, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
 #- {name: floor,   type: plane, dimensions: [32, 32],    placement: [[-1, -1,   0], [0,  0, 0]]}


stage  = doc.addObject("Part::Plane", "floor")  #https://wiki.freecad.org/Part_Plane
stage.Length     = stage.Width  = 32.
stage.Placement   = App.Placement(App.Vector(-1,   -1, 0), App.Rotation( 0, 0, 0))

scene:
 - {name: bldg1a,  type: box,   dimensions: [28, 28, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
 - {name: floor,   type: plane, dimensions: [32, 32],    placement: [[-1, -1,   0], [0,  0, 0]]}

booleanOps:
 - {name: bldgCut1, op: cut, descr: building central void, base: bldg1a, tool: bldg1b}

#Heider & Simmel 1944 variant; https://www.youtube.com/watch?v=VTNmLt7QX8E


bldg1a = doc.addObject("Part::Box",   "bldg1a")
bldg1b = doc.addObject("Part::Box",   "bldg1b")

screen1 = doc.addObject("Part::Plane", "screen1") 
screen2 = doc.addObject("Part::Plane", "screen2") 

bldg1a.Length    = bldg1a.Width = 28.; bldg1a.Height = 3.
bldg1b.Length    = bldg1b.Width = 26.; bldg1b.Height = 3.
screen1.Width    = 8
screen1.Length   = 8. / 1.77 # 1920/1080 ~= 1.77
screen2.Width    = screen1.Width
screen2.Length   = screen1.Length

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

### end ###

