# hack for moving window to 0,0 
# Brygg Ullmer, Clemson University

import platform, pygame

#WIDTH, HEIGHT  = 1024, 1024
WIDTH, HEIGHT   = 1920, 1080

if platform.system() == "Windows":
  from ctypes import windll
  hwnd = pygame.display.get_wm_info()['window']
  windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)

import pgzero

global opacitySupported
opacitySupported = False

try:    
  if int(pgzero.__version__[2]) >= 3: opacitySupported = True
except: 
  pass #hack to determine if opacity is supported; will break when pgz 2, 3, etc. arrive
### end ###
