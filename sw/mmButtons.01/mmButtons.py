#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from tkinter   import *
from functools import partial
import yaml, traceback

class enoTkiButtonArray:
  numRows,  numCols   = 2, 2
  butWidth, butHeight = 200, 200
  yamlFn              = 'mmButtons.yaml'
  yamlD      = None
  buttonDict = None
  parent     = None

  ######### constructor #########

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.loadYaml()
    self.buildUI()

  ######### default callback #########

  def defaultCb(self): print("button was pushed")

  ######### loadYaml #########

  def loadYaml(self):   
    try:
      yf = open(self.yamlFn, 'rt')
      yd = yaml.safe_load(yf)
      self.yamlD = yd

      if 'mmButtons' not in yd:
        print("loadYaml: mmButtons not found in yaml file"); return

      mmb = yd['mmButtons']
      self.buttonDict = {}

      for e in mmb: #e is for "entry"
        coord, btext, cbStr, cbArg = e['coord'], e['text'], e['cb'], e['cbArg']
        cbFunc = getattr(self,   cbStr)
        cb     = partial(cbFunc, cbArg)
        b      = Button(self.parent, text=btext, command=cb) # Create a label with words
        b.pack()

        self.buttonDict[coord] = b

    except: print("loadYaml: ignoring parsing issue"); traceback.print_exc()
   
    #example entries: 
    #mmButtons:
    #  - {coord: [0, 0], text: A, cb: defaultCb, cbArg: A}

  def buildUI(self): pass  

if __name__ == "__main__":
  root = Tk()    # Create the root (base) window 
  etba = enoTkiButtonArray(parent=root)
  #root.mainloop() # Start the event loop

### end ###
