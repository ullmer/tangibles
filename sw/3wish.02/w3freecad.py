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

scene:
 - {name: bldg1a,  type: box,   dimensions: [28, 28, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
 - {name: bldg1b,  type: box,   dimensions: [26, 26, 3], placement: [[ 0,  0,   0], [0,  0, 0]]}
 - {name: floor,   type: plane, dimensions: [32, 32],    placement: [[-1, -1,   0], [0,  0, 0]]}
 - {name: screen1, type: plane, dimensions: [ 8,  4.5],  placement: [[ 3,  3,   5], [0, 90, 0]]}
 - {name: screen2, type: plane, dimensions: [ 8,  4.5],  placement: [[ 3, 11.5, 5], [0, 90, 0]]}

booleanOps:
 - {name: bldgCut1, op: cut, descr: building central void, base: bldg1a, tool: bldg1b}

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

### end ###

