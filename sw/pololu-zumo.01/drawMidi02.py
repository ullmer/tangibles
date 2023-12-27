# Example of drawing MIDI events
# Brygg Ullmer, Clemson University
# Begun 2023-12-27

import mido, time
from mido import MetaMessage
from functools import partial
import pygame

midiValsPerOctave = 12
pixelsPerVal      = 3
vertMultiplier    = 3
midiValsTotal     = 127
midiValOctaves    = int(midiValsTotal / midiValsPerOctave)

colScaleGray = (50, 50, 50)
colScaleRed  = (100, 0,  0)
colNote      = (100, 100, 100)

#HEIGHT = midiValsTotal * pixelsPerVal
HEIGHT = 1000
WIDTH  = 1600

######################## place window @ 0,0 ####################

#magic for placing at 0,0
import platform, pygame
if platform.system() == "Windows":
  from ctypes import windll
  hwnd = pygame.display.get_wm_info()['window']
  windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)

######################## cursor ########################

class cursor:
  cursorPos = 0

  def draw(self): 
    screen.draw.line((self.cursorPos, 0), (self.cursorPos, HEIGHT), colScaleRed)
    if self.cursorPos == WIDTH: 
      self.cursorPos = 0
      animate(self, cursorPos=WIDTH, duration=20.)

######################## noteStore ########################

class noteStore:
  notes = []
  curs  = None #cursor     
  
  ####################### constructor #######################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not
  
  def clearNotes(self): self.notes = []

  ####################### add note #######################

  def addNote(self, noteVal, xCoord=None): 
    if xCoord is None: xCoord = self.curs.cursorPos
    self.notes.append([noteVal, xCoord])

  ####################### draw #######################

  def draw(self):
    for note in self.notes:
      noteVal, xCoord = note
      self.drawNote(noteVal, xCoord)
   
  def drawNote(self, noteVal, xCoord=None):
    x, y = xCoord, HEIGHT - (pixelsPerVal * noteVal * vertMultiplier) 
    w, h = pixelsPerVal, pixelsPerVal
    #print("r:", x,y,w,h)
    r    = pygame.Rect(x,y,w,h)
    screen.draw.filled_rect(r, colNote)

######################## draw grid ########################

def drawGrid():
  x1, x2 = 0, WIDTH
  y      = pixelsPerVal

  for octIdx in range(midiValOctaves):
    screen.draw.line((x1,y), (x2,y), colScaleGray)
    y += midiValsPerOctave * pixelsPerVal * vertMultiplier

######################## main ########################

c  = cursor()
ns = noteStore(curs=c)
animate(c, cursorPos=WIDTH, duration=20.)
  
#ns.addNote(10, 10)
#ns.addNote(20, 20)
#ns.addNote(30, 30)

######################## draw ########################

def draw():
  screen.fill((10, 10, 20))
  drawGrid()
  ns.draw()
  c.draw()

######################## mido play ########################

class pgzMidoPlayer:
  midoObjIter = None
  midoObj     = None
  midoOut     = None  
  ns          = None #notestore

  start_time = None
  input_time = None
  queuedMsg  = None

  ####################### constructor #######################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor

  ####################### play #######################

  def play(self):

    print("mpnow")

    #variant of https://github.com/mido/mido/blob/main/mido/midifiles/midifiles.py
    self.start_time  = time.time()
    self.input_time  = 0.0
    self.midoObjIter = midoObj.__iter__()

    self.serviceMessages()

  ####################### play #######################

  def resume_play(self):
    msg = self.queuedMessage
    self.midoOut.send(msg)

    try:    self.ns.addNote(int(msg.note))
    except: print(msg)

    self.serviceMessages()

  ####################### play #######################

  def serviceMessages(self):
    while True:
      msg = self.midoObjIter.__next__()
      if msg is None: break
      self.input_time += msg.time

      playback_time          = time.time() - self.start_time
      duration_to_next_event = self.input_time  - playback_time

      if duration_to_next_event > 0.0:
        self.queuedMessage = msg
        clock.schedule(self.resume_play, duration_to_next_event)
        break
      else: 
        if isinstance(msg, MetaMessage): continue 
        try:    self.ns.addNote(int(msg.note))
        except: print(msg)

        self.midoOut.send(msg)

######################## midi setup ########################

outport = None
for port in mido.get_output_names():
  outport = port; print("output:", outport)

mfn     = '3400themerrypheastevenritchie.mid'
midoOut = mido.open_output(outport)
midoObj = mido.MidiFile(mfn)

pmp = pgzMidoPlayer(midoObj=midoObj, midoOut=midoOut, ns=ns)

print(1)
pmp.play()
print(2)

### end ###
