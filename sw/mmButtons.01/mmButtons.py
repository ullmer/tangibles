#
# Brygg Ullmer, Sarah Sears, and Uzayr Syed
# Begun 2025-04-11

# https://en.wikipedia.org/wiki/Tkinter

from tkinter import *

class enoTkiButtonArray:
  numRows,  numCols   = 2, 2
  butWidth, butHeight = 200, 200
  yamlFn              = 'mmButtons.yaml'
  yamlD  = None

  ######### constructor #########

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    self.loadYaml()
    self.builtUi()

  def defaultCb(self): print("button was pushed")

  def loadYaml(self):   

  def buildUI(self):   


b    = Button(root, text="Hello, world!", command=helloCB) # Create a label with words
b.pack()                                                   # Put the label into the window
root.mainloop()                                            # Start the event loop

if __name__ == "__main__":
  root = Tk()    # Create the root (base) window 
  etba = enoTkiButtonArray



### end ###
