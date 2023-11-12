# Tkinter grid of buttons
# Brygg Ullmer, Clemson University
# Begun 2023-09-18

# https://www.activestate.com/resources/quick-reads/how-to-position-widgets-in-tkinter/
# https://docs.python.org/3/library/tk.html
# https://www.tutorialspoint.com/python/tk_grid.htm
# https://www.tutorialspoint.com/python/tk_button.htm

import tkinter as tk           #Tkinter graphical interface
import PIL.Image, PIL.ImageTk #image manipulation package
from functools    import partial
  
##################################################### 
############# enodia Tkinter image grid #############
##################################################### 

class enoTkImgGrid:

  rows, columns  = 8, 9    #initially, hardcode a series of defaults
  w, h           = 94, 94
  windowGeometry = "900x800-0-0"
  color1         = (200, 100,   0)
  color2         = (200,   0, 200)
  root           = None
  hideTitlebar   = False
  buttonState    = None
  buttonTk       = None
  imagesDict     = None
  imgPrefix      = None
  padX           = 15
  padY           = 15
  bgImgFn        = None

  autostartMainloop = False

  ############# constructor #############

  def __init__(self, imgPrefix, **kwargs):

    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    self.imgPrefix = imgPrefix 
    self.buildUI()

  #################### build user interface ####################

  def buildUI(self):
  
    self.root = tk.Tk()
    self.root.title("Interactive grid example")
    self.root.geometry(self.windowGeometry)
    if self.hideTitlebar: self.root.overrideredirect(1) #hide window decorations ~= titlebar
  
    self.buttonState = {}
    self.buttonTk    = {}

    self.buildColorGrid()

    if self.autostartMainloop: self.root.mainloop()   

  #################### build image grid ####################

  def buildColorGrid(self):

    # images need to be held an a data structure, or else they will be garbage collected
    self.imagesDict = {}

    #background image, per 
    # https://stackoverflow.com/questions/62430477/how-to-set-a-background-image-in-tkinter-using-grid-only

    for i in range(self.rows):
      for j in range(self.columns):
        coord  = (i, j)
        cb     = partial(self.toggleCB, coord) #e.g., https://www.blog.pythonlibrary.org/2016/02/11/python-partials/
        button = tk.Button(self.root, text='', command=cb) 
        self.buttonState[coord] = False
        self.buttonTk[coord]    = button
        button.grid(row=i, column=j, padx=self.padX, pady=self.padY)
  
  ############### button toggle callback ############### 
  
  def toggleCB(self, coord):
    if self.buttonState[coord]: 
      self.buttonState[coord] = False
      print("toggleCB on %s: off" % str(coord))
      #self.buttonTk[coord].configure(image=imTk1)
    else:
      self.buttonState[coord] = True
      print("toggleCB on %s: on" % str(coord))
      #self.buttonTk[coord].configure(image=imTk2)
  
### end ###
  
