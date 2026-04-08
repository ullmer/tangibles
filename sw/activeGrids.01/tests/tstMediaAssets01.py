# Test of enodia media assets (01)
# Brygg Ullmer, Clemson University
# Begun 2026-03-31

import sys; sys.path.append("../py")
from enoMediaAssets import *

url = "https://computing.clemson.edu/~bullmer/images/chessSofonisbaAnguissola1555o.jpg"
lfn = "chessSofonisbaAnguissola1555o.jpg"

ema1 = EnoMediaAsset(mediaUrl = url, mediaFn = lfn,
         allowInsecure=True,                   # explicit, visible
         trustPolicy="clemson-legacy-hosting") # recorded in trust log


### end ###
