import yaml
yfn = 'cspTagAkaMin01.yaml'
yf  = open(yfn, 'rt')
yd  = yaml.safe_load(yf)

#a2, a2 is from top-left; but 0, 1 from bottom-left

def mapCoord(coord):
  row = ord(coord[0]) - ord('a')
  col = int(coord[1])
  row2 = 7-row
  result = row2*8 + col
  #print(row, col, result)
  return result

for tag in yd:
  coord = yd[tag]
  #print(tag, coord)
  padId = mapCoord(coord)
  print('%s: %s' % (tag, padId))

### end ###
