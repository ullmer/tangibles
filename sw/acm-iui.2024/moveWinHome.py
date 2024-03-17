import platform, pygame
import os

#WIDTH  = 1024
#HEIGHT = 1024

WIDTH  = 2160
HEIGHT = 2160

if platform.system() == "Windows":
  from ctypes import windll
  hwnd = pygame.display.get_wm_info()['window']
  windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)
else:
  #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
  #screen = pygame.display.set_mode((100,100))

  w, h = pygame.display.get_surface().get_size()
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
  os.environ['SDL_VIDEO_CENTERED'] = '1'

### end ###
