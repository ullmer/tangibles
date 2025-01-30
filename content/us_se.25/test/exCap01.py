from machine import I2C
i2c=I2C(0, scl=Pin(5), sda=Pin(4))
mpr=mpr121.MPR121(i2c, 0x5A)
mpr.touched()
