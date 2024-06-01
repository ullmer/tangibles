# SolidPython2 synthesis of rim textual expression
# Brygg Ullmer, Clemson University
# Begun 2024-05-31

#Builds upon:
#https://github.com/jeff-dh/SolidPython/blob/master-2.0.0-beta-dev/solid2/examples/11-fonts.x.py

#from solid2 import text, register_font, set_global_viewport_translation, cube, translate, rotate
#from solid import *
#from solid.utils import *

from solid2 import *

import yaml, sys, math, traceback

verbose = False

yfn = '../../yaml/rim02.yaml' #refactor to command-line argument
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)
#if verbose: print(yd)

try:
  ydr = yd['rim']
except:
  print("rim not found in source yaml"); sys.exit(-1)

#################### extract text angles #################### 

def extractField(ydr, fieldName):
  result = []
  try:
    angles = ydr['angles']

    for term in angles:
      if fieldName in term:
        value = term[fieldName]
        result.append(value)
  except:
    print("problem in extraction of", fieldName); 
    traceback.print_exc(); #sys.exit(-1)
  return result

def extractTextAngles(ydr): return extractField(ydr, 'centroidA')
def extractTextStrs(ydr):   return extractField(ydr, 'word')

#################### extract text angles #################### 

def synthTextAngles(angles, textStrs, ellipseWidth, ellipseHeight):
  result = None

  lenAng, lenTxts = len(angles), len(textStrs)
  if lenAng != lenTxts:
    print("synthTextAngles issue: length of lists angles and texts differs! Aborting."); sys.exit(-1)

  for i in range(lenAng):
    angle, textStr = angles[i], textStrs[i]
    textGeom       = text(text=textStr, size=.3) #, font=
    # https://github.com/jeff-dh/SolidPython/blob/master-2.0.0-beta-dev/solid2/core/builtins/openscad_primitives.py

    angleRadians = math.radians(angle)
    x       = ellipseWidth  * math.cos(angleRadians)
    y       = ellipseHeight * math.sin(angleRadians)
    length  = math.hypot(x,y)

    textGeomSc = scale([1,1,.1])(textGeom)
    textTrans  = translate([length,0,0])(textGeomSc)
    textRot    = rotate(a=angle)(textTrans)

    if result == None: result =  textRot
    else:              result += textRot

  return result

#################### main #################### 

try:
  fontSide = ydr['fonts']['side']
  typeface = fontSide['face']
  fontSize = fontSide['size']
except:
  print("problems accessing font data from source yaml")
  traceback.print_exc(); #sys.exit(-1)

try:
  ellipseDimensions = ydr['dimensions']['OD']
  ellipseWidth, ellipseHeight = ellipseDimensions
except:
  print("problems accessing ellipse dimensions from source yaml")
  traceback.print_exc(); sys.exit(-1)

if verbose: print("fonts:", typeface, fontSize)

angles   = extractTextAngles(ydr)
textStrs = extractTextStrs(ydr)
if verbose: print(angles)

geom = synthTextAngles(angles, textStrs, ellipseWidth, ellipseHeight)
print(geom)

register_font("fonts/" + typeface)
set_global_viewport_translation([700, 900, 200])
text(font="Rich Eatin'", text="blablub").save_as_scad()

### end ###
