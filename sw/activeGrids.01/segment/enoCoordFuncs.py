def det(a, b): return a[0] * b[1] - a[1] * b[0]

################ get line intersection ################ 

# getLineIntersection via CoPilot, in response to:
# python code for determining the intersecting point between two line segments.  
# it should accept parameters A, B, C, D, which are two-coordinate tuples.  
# One segment spans from A to B; the other, from C to D.  
# The intersecting vertex should be returned.

def getLineIntersection(a,b,c,d):
  if a is None or b is None or c is None or d is None:
    print("getLineIntersection passed argument of None"); return None

  xdiff = (a[0] - b[0], c[0] - d[0])
  ydiff = (a[1] - b[1], c[1] - d[1])

  div  = det(xdiff, ydiff)
  if div == 0: return None  # Lines do not intersect

  d = (det(a, b), det(c, d))
  x = det(d, xdiff) / div
  y = det(d, ydiff) / div
  return (x, y)

def getLineIntersection2(l1, l2):
  if l1 is None or l2 is None:
    print("getLineIntersection2 passed argument of None"); return None

  a, b = l1; c, d = l2
  result = getLineIntersection(a,b,c,d)
  return result

################ get bounding box ################ 

def getBoundingBox(a,b,c,d):
  xvals = [a[0], b[0], c[0], d[0]]
  yvals = [a[1], b[1], c[1], d[1]]

  x1, y1 = min(xvals), min(yvals)
  x2, y2 = max(xvals), max(yvals)

  result = [(x1,y1), (x2, y2)]
  return result

################ get coord average ################ 

def getCoordAvg1(a,b,c,d): #heuristic approximation for center
  xs, ys = 0, 0
  for coord in [a,b,c,d]: xs += coord[0]; ys += coord[1]
  return (xs/4., ys/4.)

################ main ################ 

if __name__ == "__main__":

  a,b,c,d = [(0,0), (1,1), (1,0), (0,3)]
  r = getLineIntersection(a,b,c,d)
  print(r)

  s = getBoundingBox(a,b,c,d)
  print(s)

### end ###
