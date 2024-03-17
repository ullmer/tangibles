import platform, pygame

#WIDTH  = 1024
#HEIGHT = 1024

WIDTH  = 2160
HEIGHT = 2160

if platform.system() == "Windows":
  from ctypes import windll
  hwnd = pygame.display.get_wm_info()['window']
  windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)

### end ###
