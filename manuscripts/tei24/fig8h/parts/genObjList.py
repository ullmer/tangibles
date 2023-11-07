# Generate object list of FreeCAD elements in model (exported as Obj from Blender)
# Brygg Ullmer, Clemson University
# Begun 2023-10-30

modelName = 'hexPlinth62a'
yamlFn    = 'c:/git/tangibles/manuscripts/tei24/fig8h/hexPlinth62a.yaml'

doc     = App.getDocument(modelName)
objList = doc.Objects

yf      = open(yamlFn, 'wt')

for obj in objList:
  label = str(obj.Label)
  yf.write(" - %s\n" % label)

yf.close()

### end ###
