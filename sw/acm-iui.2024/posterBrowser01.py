# Poster++ tangibles-supported browser code
# Brygg Ullmer, Clemson University
# Begun 2024-03-17

WIDTH  =
HEIGHT = 

class posterBrowser:
  topBlockFn = 'full_res/top_block01'
  upperHlBox = 'full_res/upper_highlight_box'

  arrayDim = [8, 8]
  panelWidth  = None
  panelHeight = None

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.imgSrc = Image.open(self.imgSrcFn)
    #self.imgSrc.show()
    self.panelWidth, self.panelHeight = self.imgSrc.size
    self.tileWidth  = self.panelWidth /self.arrayDim[0]
    self.tileHeight = self.panelHeight/self.arrayDim[1]

  def extractPane(self, tileCol, tileRow):
    x1 = self.tileWidth  * tileCol
    y1 = self.tileHeight * tileRow
    x2 = self.tileWidth  * (tileCol+1)
    y2 = self.tileHeight * (tileRow+1)

    self.targPane = self.imgSrc.crop((x1, y1, x2, y2))
    return self.targPane
    #self.targPane.show()
  
tfnPre = "gridMap03k5"
srcFn  = tfnPre + '.png'
tp = tiledPanel(imgSrcFn=srcFn)

for i in range(tp.arrayDim[0]):
  for j in range(tp.arrayDim[1]):
    targPane = tp.extractPane(i,j)
    fn = tp.imgSrcFn; 
    tfn = '%s/%i%i.png' % (tfnPre, i, j)
    print(tfn)
    targPane.save(tfn)

### end ###
