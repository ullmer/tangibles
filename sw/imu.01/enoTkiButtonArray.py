# Enodia Tkinter-based button array with YAML config (including callbacks)
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from tkinter   import *
from functools import partial
import yaml, traceback

class enoTkiButtonArray:
  numRows,  numCols   = 2, 2
  butWidth, butHeight = 6, 2
  butTextWrapLength   = 200
  butFont        = ('Sans','60','bold')
  yamlFn       = 'mm01.yaml'
  yamlD        = None
  buttonDict   = None
  parent       = None
  defaultCbArg   = "default argument"
  defaultBgColor = 'gray'

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
      self.yamlD = yaml.safe_load(yf)

      yd = self.yamlD
      if 'numRows' in yd: self.numRows = yd['numRows']
      if 'numCols' in yd: self.numCols = yd['numCols']
    except: print("loadYaml: ignoring issue"); traceback.print_exc()

    #example entries: 
    #buttons:
    #  - {coord: [0, 0], text: A, cb: defaultCb, cbArg: A}

  ######### build ui #########

  def buildUI(self): 
    try:
      yd = self.yamlD 

      if 'buttons' not in yd:
        print("buildUI: buttons not found in yaml file"); return

      mmb = yd['buttons']
      self.buttonDict = {}

      for e in mmb: #e is for "entry"
        coord, btext, cbStr, cbArg = e['coord'], e['text'], e['cb'], e['cbArg']

        cb = None

        try: 
          cbFunc = getattr(self, cbStr)  #first, see if the callback str defines a method within this class
          cb     = partial(cbFunc, cbArg)
        except:                             #and if not, see if it references a function within global scope
          try: 
            cbFunc = globals()[cbStr]    #this may be unsafe
            cb     = partial(cbFunc, cbArg)
          except: 
            #print("globals: ", str(globals()))
            cbFunc, cbArg = self.defaultCb, self.defaultCbArg
            cb            = partial(cbFunc, cbArg)

        w, h   = self.butWidth, self.butHeight

        c, f, bwl = self.defaultBgColor, self.butFont, self.butTextWrapLength   
        if 'bg' in e: c = e['bg']; #print("bg:" + str(c))
        #else: print("no background color specified")

        b    = Button(self.parent, text=btext, command=cb, width=w, height=h, bg=c, font=f, wraplength=bwl)
        i, j = coord
        b.grid(row = i, column = j)
        #b.pack()

        self.buttonDict[str(coord)] = b

    except: print("buildUI: ignoring issue"); traceback.print_exc()
  
######### default main #########

if __name__ == "__main__":
  root = Tk()    # Create the root (base) window 
  etba = enoTkiButtonArray(parent=root)
  root.mainloop() # Start the event loop

### end ###
