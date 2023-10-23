# First validation of Python port of 1995 3wish code
# Brygg Ullmer, Clemson University
# Original code begun fall 1995; here, 2023-10-20

import FreeCAD as App
import FreeCADGui as Gui
import pivy.coin as coin
import sys

sys.path.append('c:/git/designThinking/2023/hccFundamentals/3wish')
from w3core  import *
from w3shift import *

view, doc, sg, root = genViewDocSgRoot()

wedge1 = doc.addObject("Part::Wedge", "myWedge") #https://wiki.freecad.org/Part_Wedge#Scripting
wedge1.Placement = App.Placement(App.Vector(0, 0, 1), App.Rotation(0, 0, 0))

wedge2 = doc.addObject("Part::Wedge", "myWedge") #https://wiki.freecad.org/Part_Wedge#Scripting
wedge2.Placement = App.Placement(App.Vector(0, 3, 1), App.Rotation(0, 0, 15))

doc.recompute()

Gui.runCommand('Std_ViewZoomOut',0)
Gui.SendMsgToActiveView("ViewFit")

### end ###
