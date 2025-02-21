from enoNfcRC522 import *

print("nfc tag reader active")
enr = enoNfcRC522(verbose=True)

while True: 
  enr.poll()
  time.sleep(.1)

### end ###

