#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from tkinter   import *
from functools import partial
import yaml, traceback

class enoTkiButtonArray:
  numRows,  numCols   = 2, 2
  butWidth, butHeight = 15, 5
  yamlFn       = 'mmButtons.yaml'
  yamlD        = None
  buttonDict   = None
  parent       = None
  defaultCbArg = "default argument"

  ######### constructor #########

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.loadYaml()
    self.buildUI()

  ######### default callback #########

  def defaultCb(self, arg): print("button was pushed, arg " + str(arg))

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

        cb = None

        try: 
          cbFunc = getattr(self, cbStr)  #first, see if the callback str defines a method within this class
          cb     = partial(cbFunc, cbArg)
        except:                             #and if not, see if it references a function within global scope
          try: 
            cbFunc = globals()[cbStr]
            cb     = partial(cbFunc, cbArg)
          except: 
            cbFunc, cbArg = self.defaultCb, self.defaultCbArg
            cb            = partial(cbFunc, cbArg)

        w, h   = self.butWidth, self.butHeight
        b      = Button(self.parent, text=btext, command=cb, width=w, height=h)
        b.pack()

        self.buttonDict[str(coord)] = b

    except: print("loadYaml: ignoring parsing issue"); traceback.print_exc()
   
    #example entries: 
    #mmButtons:
    #  - {coord: [0, 0], text: A, cb: defaultCb, cbArg: A}

  def buildUI(self): pass  

if __name__ == "__main__":
  root = Tk()    # Create the root (base) window 
  etba = enoTkiButtonArray(parent=root)
  root.mainloop() # Start the event loop

### end ###
