# hack for moving window to 0,0 
# Brygg Ullmer, Clemson University

import platform, pygame

#WIDTH, HEIGHT  = 1024, 1024
WIDTH, HEIGHT   = 1920, 1080

if platform.system() == "Windows":
  from ctypes import windll
  hwnd = pygame.display.get_wm_info()['window']
  windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)

### end ###
