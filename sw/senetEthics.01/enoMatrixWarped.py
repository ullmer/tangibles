# Experiment in representing a gridded workspace (virtual or physical)
# Brygg Ullmer, Clemson University
# Begun 2026-03-27

from enoMatrix             import *
from enoSegmentedImgCoords import *

Matrix = List[List[Any]]

class EnoMatrixWarped(EnoMatrix):

  ############# constructor #############

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    super().__init__()

### end ###
