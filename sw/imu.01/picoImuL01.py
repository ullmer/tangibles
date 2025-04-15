from adafruit_lsm6ds.lsm6ds3 import LSM6DS3 as LSM6DS
import time
import board
import busio

i2c = busio.I2C(board.GP7, board.GP6)
accel_gyro = LSM6DS(i2c, address=0x6b)

while True:
  a = accel_gyro.acceleration
  g = accel_gyro.gyro
  agJson = "{s:ag1, a:[%2.2f,%2.2f,%2.2f], g:[%2.2f,%2.2f,%2.2f]}" % (a+g)
  print(agJson)
  time.sleep(1.)
