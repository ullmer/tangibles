# Senet ethics example
# Brygg Ullmer, Clemson University
# Begun 2026-03-24

WIDTH, HEIGHT=1535,1180

a  = Actor('backdrops/senet03k')

peopleAbbrev = ['gel', 'jgh', 'tr', 'fdr', 'er', 'rf']
people = []; x, y = 300, 500; dx = 75
for pa in peopleAbbrev: 
  imgFn = "people/" + pa
  p = Actor(imgFn); people.append(p)
  p.pos = (x,y); x+= dx

def draw(): 
  a.draw(); 
  for p in people: p.draw()

### end ###
