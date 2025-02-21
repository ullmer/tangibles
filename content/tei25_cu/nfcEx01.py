from enoNfcRC522 import *

print("\n***** Scan your RFid tag/card *****\n")
enr = enoNfcRC522(verbose=True)

while True: 
  enr.poll()
  time.sleep(.1)

### end ###

