# SolidPython2 synthesis of rim textual expression
# Brygg Ullmer, Clemson University
# Begun 2024-05-31

#Builds upon:
#https://github.com/jeff-dh/SolidPython/blob/master-2.0.0-beta-dev/solid2/examples/11-fonts.x.py

from solid2 import text, register_font, set_global_viewport_translation
import yaml, sys, traceback

verbose = True

yfn = '../yaml/rim02.yaml' #refactor to command-line argument
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)
#if verbose: print(yd)

try:
  ydr = yd['rim']
except:
  print("rim not found in source yaml"); sys.exit(-1)

#################### extract text angles #################### 

def extractTextAngles(ydr):
  result = []
  try:
    angles = ydr['angles']

    for term in angles:
      if 'centroidA' in term:
        centroidAngle = term['centroidA']
        result.append(centroidAngle)
  except:
    print("problem in extraction of rim text angles"); 
    traceback.print_exc(); #sys.exit(-1)
  return result

#################### extract text angles #################### 

def synthCubicApprox(rootNode, angles):
  d = .002 #mm
  testCube  = cube([d,d,d])
  translate = translate([35, 0, 0]) #mm
 
  result = None

  for angle in angles:
    rotCube = rotate(a=angle)(testCube)
    trCube  = translate(rotCube)
    if result == None: result =  trCube
    else:              result += trCube

  return result

#################### main #################### 

angleList = extractTextAngles(ydr)

try:
  fontSide = ydr['fonts']['side']
  typeface = fontSide['face']
  fontSize = fontSide['size']
except:
  print("problems accessing font data from source yaml")
  traceback.print_exc(); #sys.exit(-1)

if verbose: print("fonts:", typeface, fontSize)

angles = extractTextAngles(ydr)
if verbose: print(angles)

register_font("fonts/" + typeface)

#set_global_viewport_translation([700, 900, 200])

#text(font="Rich Eatin'", text="blablub").save_as_scad()

### end ###
