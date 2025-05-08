# Interaction panel code
# Brygg Ullmer, Clemson University
# Begun 2024-10-09

import sys, os, traceback

############# enodia interaction panel #############

class enoIpanel:

  rows, cols = 8, 8
  verbose    = False
  colorMap   = None

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

  ############# error, msg #############

  def err(self, msg): print("enoIpanel error: " + str(msg)); traceback.print_exc(); 
  def msg(self, msg): print("enoIpanel msg: "   + str(msg))

### end ###
