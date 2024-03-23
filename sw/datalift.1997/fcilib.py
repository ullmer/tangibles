# FreeCAD/Coin/Inventor support routines 
# Brygg Ullmer, Clemson University
# Begun 2022-07-02

from pivy import coin
sg = FreeCADGui.ActiveDocument.ActiveView.getSceneGraph()
print(sg)

for node in sg.getChildren():
    print(node)

#col = coin.SoBaseColor()
#col.rgb = (1, 0, 0)
tex = coin.SoTexture2()
#tex.filename = 'c:/tmp/unsdg.png'
tex.filename = 'c:/tmp/unsdg-transpWh01.png'
tex.model    = 'BLEND'

cube  = coin.SoCube()
plane = coin.SoPlane()
node = coin.SoSeparator()
#node.addChild(col)
node.addChild(tex)
#node.addChild(cube)
node.addChild(plane)
sg.addChild(node)

### end ###

