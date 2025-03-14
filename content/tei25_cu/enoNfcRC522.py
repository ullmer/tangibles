# Abstraction around RC522 CircuitPython wrapper
# Brygg Ullmer, Clemson University
# Begun 2025-02-21

# Builds upon: 
# https://tutorial.cytron.io/2022/01/11/interface-rfid-rc522-reader-using-maker-pi-pico-and-circuitpython/
# https://github.com/domdfcoding/circuitpython-mfrc522]
  
import time

###################### Enodia NFC abstraction ######################

class enoNfc:
  hardwareActive = True # False activates virtual/etc. version
  rfidVal        = None
  rfidPresent    = None

  def __init__(self, controllerName, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not

    self.rfidVal = 0; self.rfidPresent=False

  def poll(self): return self.rfidVal

###################### Enodia NFC binding to RC522 ######################

class enoNfcRC522(enoNfc):

  sck  = board.GP2 
  mosi = board.GP3 
  miso = board.GP4 
  csP  = board.GP26
  rstP = board.GP6

  setGain     = False
  antennaGain = 0x07
  verbose     = False

  spi, cs, rst, rfid            = [None] * 4
  prev_data, prev_time, timeout = [None] * 3

  ############# constructor #############

  def __init__(self, controllerName, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

    super().__init__()

  ############# make hardware-specific imports if hardware present #############

  def hardwareImports(self):
   if hardwareActive: import board, digitalio, simpleio, busio, mfrc522

  ############# initiate NFC #############

  def initHW(self):
    sc, mo, mi = self.sck, self.mosi, self.miso
    self.spi   = busio.SPI(sc, MOSI=mo, MISO=mi)

    self.cs  = digitalio.DigitalInOut(self.csP)
    self.rst = digitalio.DigitalInOut(self.rstP)

    self.rfid = mfrc522.MFRC522(self.spi, self.cs, self.rst)      
    if self.setGain: rfid.set_antenna_gain(self.antennaGain << 4)

    self.prev_data = ""; self.prev_time = 0; self.timeout = 1

  ############# poll NFC #############

  def poll(self):
    is self.rfid is None: self.msg("poll called, but RFID/NFC not initialized"); return None

    (status, tag_type) = self.rfid.request(self.rfid.REQALL)

    if status  == self.rfid.OK: (status2, raw_uid) = self.rfid.anticoll()  
    if status2 == self.rfid.OK:
      a, b, c, d = raw_uid[0:3]
      self.rfidVal = "{:02x}{:02x}{:02x}{:02x}".format(a,b,c,d)
      self.rfidPresent = True

      if rfid_data != self.prev_data:
        self.prev_data = self.rfidVal
        if self.verbose: print("Card detected! UID: {}".format(rfid_data))

      prev_time = time.monotonic()
      return self.rfidVal

    else:
      if time.monotonic() - self.prev_time > self.timeout: 
        self.prev_data = ""; self.rfidPresent=False; return None

      return self.rfidVal #this may need rethinking

if __name__ == "__main__":

  print("\n***** Scan your RFid tag/card *****\n")
  enr = enoNfcRC522(verbose=True)

  while True: enr.poll(); time.sleep(.1)

### end ###
