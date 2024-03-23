# Transform plurality of [incr Tcl] object-parameter metadata from May 14, 1998
#  Inter-Design Workshop (IDW) class project with Jay Lee and Kerstin Hoegger 
#  (Instructors: Hiroshi Ishii and John Maeda; TA: Paul Yarin) to YAML
# Several week class project: "Datalift" cyberphysical genkan
#
# Brygg Ullmer, Clemson University
# Begun 2022-06-29

#source format (plurality of .rgb files; same name as source image)
## building picture structure auto-written Thu May 14 12:44:01 EDT 1998
#
#-whichFloor {floor4}
#-whichYear {1992}
#-floorCoord {0.864865 0.0988764}
#-imageAspect {portrait}
#-paneAngle {0}
#-paneHeight {6.}
#-paneWidth {8.}
#-imageFilePrefix {ml-oimages/}
#-imageFileName {91-11-machover.rgb}
#-structFilePrefix {pic-structs}
#-structFileName {91-11-machover.rgb}
#-baseElev {}

#to:
#- 91-11-machover: {whichFloor: floor4, whichYear: 1992, imageAspect: portrait, 
#                   imageFilePrefix: ml-oimages/, imageFilename: 91-11-machover.png, 
#                   paneAngle: 0, paneHeight: 6, paneWidth: 8, baseElev: 0,
#                    metadataDate: }
#  

#################### import metadata ####################

import glob

global origMetadata, yamlExportPat
origMetadata = {}

filenames = glob.glob('*.rgb')
for fn in filenames:
  f = open(fn, 'r')
  origMetadata[fn] = f.readlines()
  f.close()

yamlExportPat = """- %s: {whichFloor: %s, whichYear: %s, imageAspect: %s, 
             imageFilePrefix: %s, imageFilename: %s,
             paneAngle: %s, paneHeight: %s, paneWidth: %s, baseElev: %s,
             metadataDate: %s}
"""

#################### metadata to yaml ####################

def metadata2yaml(fn):
  global origMetadata, yamlExportPat

  lines = origMetadata[fn]; idx = 0
  metadata = {}

  paramOrder = ['fn', 'whichFloor', 'whichYear', 'imageAspect',  
                'imageFilePrefix', 'imageFilename', 'paneAngle', 
                'paneHeight', 'paneWidth', 'baseElev', 
                'metadataDate']

  metadata['fn'] = fn[:-4]
  for line in lines:
    idx += 1
    if idx == 1: 
      startIdx = line.find('auto-written ')
      metadata['metadataDate'] = line[startIdx+13:-1]

    if idx > 2: 
      spaceIdx = line.find(' ')
      paramName = line[1:spaceIdx]
      paramVal  = line[spaceIdx+2:-2]
      #print("%s:%s" % (paramName, paramVal))
      metadata[paramName] = paramVal

  try:
    ifn  = metadata['imageFileName']
    ifn2 = ifn[:-3] + 'png'
    metadata['imageFilename'] = ifn2
    vals = []
    for key in paramOrder: vals.append(metadata[key])
    print(yamlExportPat % tuple(vals))
  except: pass

#################### main ####################

for fn in filenames:
  metadata2yaml(fn)

### end ###
