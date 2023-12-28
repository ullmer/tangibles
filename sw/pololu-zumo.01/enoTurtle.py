# Extended interaction support for Python LOGO turtle supports
# In time, hopefully allow physical robot, 3D graphics, and VR variations
# By Brygg Ullmer, Clemson University
# Begun 2022-08-01
# Reworked for Pololu Zumo interoperability on 2023-12-28

engines = ['turtle', 'zumo']
engine  = 'zumo'

import traceback

################ Standard Python turtle bindings ################ 

if engine == 'turtle': 
  import turtle
  turtle.title('Turtles in motion')
  turtle.setup(width=800, height=800)

  global t
  t = turtle.Turtle()

  turtle.bgcolor("black") #make the background color black
  t.color("orange")  #make the "pen color" orange
  t.pensize(10)      #choose a pen width of 10

################ Zumo + friends support library ################ 

if engine == 'zumo': import Timer 

class enoTurtleZumo:
  #https://docs.micropython.org/en/latest/library/machine.Timer.html

  timr         = None # timer
  motorSpeed   = 1500
  motor        = None
  multRot      = 10
  multForwBack = 10
  
  ####################### constructor #######################

  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) #allow class fields to be passed in constructor
    #https://stackoverflow.com/questions/739625/setattr-with-kwargs-pythonic-or-not

    if engine=='zumo'::
      self.timr = Timer()
      self.motors = robot.Motors()

  ####################### show error #######################

  def err(self, msg):
    if engine!='zumo': print('enoTurtleZumo proxy error:', msg)

  ####################### schedule callback #######################

  def scheduleCb(self, periodMs, callback):
    if engine=='zumo'::
      self.timr.init(mode=Timer.ONE_SHOT, period=periodMs, callback=callback)
    else: 
      self.err('scheduleCb: no zumo binding')

  ####################### stop motors #######################

  def stopMotors(self, when=0): 
    if engine=='zumo': 
      if when == 0: self.motors.set_speeds(0, 0) #now
      else:         self.scheduleCb(when, self.stopMotors)

  ####################### turn right #######################

  def right(self, units):
    if engine=='zumo': 
      self.motors.set_speeds(0, self.motorSpeed)
      self.stopMotors(units * self.multRot)

  ####################### turn right #######################

  def left(self, units):
    if engine=='zumo': 
      self.motors.set_speeds(self.motorSpeed, 0)
      self.stopMotors(units * self.multRot)

  ####################### turn right #######################

  def left(self, units):
    if engine=='zumo': 
      self.motors.set_speeds(self.motorSpeed, 0)
      self.stopMotors(units * self.multRot)

  ####################### go forward #######################

  def fd(self, units):
    if engine=='zumo': 
      self.motors.set_speeds(self.motorSpeed, self.motorSpeed)
      self.stopMotors(units * self.multForwBack)

  ####################### go forward #######################

  def bk(self, units):
    if engine=='zumo': 
      self.motors.set_speeds(-1 * self.motorSpeed, -1 * self.motorSpeed)
      self.stopMotors(units * self.multForwBack)

################ initiations ################ 

if engine == 'zumo':   
  from zumo_2040_robot import robot
  t = enoTurtleZumo()

##### Create shortcuts for frequent commands (cmds)
cmds       = {'r': t.right, 'l': t.left, 'f': t.fd, 'b': t.bk, 'c': t.circle,
              'u': t.penup, 'd': t.pendown}


patterns   = {'-': 'u f110 d',        # scoot  forward a bit, no marks
              '*': 'f200 r144 ' * 5,  # repeat star-leg 5 times
              'P': 'r90 f130 b100 f50 l90 c40,180 r180',
              'C': 'c60,180', 'V': 'f130 r140 f130', 'A': 'f130 r140 f130'}

################# command sequence #################

class enoCommandSeq:
  commandSeq = []
  commandIdx = 0

  def registerSeq(self, cmdSeq): self.commandSeq = cmdSeq.split() #break apart 'r90 f130' into ['r90', 'f130']

################# Follow Patterns #################

def followPattern(patTxt): #follow a command sequence defined by pattern text
  global cmds, pattern, engine

  commands = patTxt.split() #break apart 'r90 f130' into ['r90', 'f130']

  for command in commands:
    try:
      cmdChar = command[0];
      if cmdChar in patterns:
        patTxt = patterns[cmdChar]
        followPattern(patTxt)
        continue

      args = []

      if len(command) > 1:
        argTxt1 = command[1:] # break text into two parts
        if argTxt1.find(','): argTxt2 = argTxt1.split(',') #handle commas
        else:                 argTxt2 = [argTxt1]

        for arg in argTxt2: args.append(int(arg)) # turn letters into numbers

      if cmdChar in cmds:
        cmd = cmds[cmdChar]

        #if len(args) == 0: print("Running", cmdChar); cmd()
        #if len(args) == 1: print("Running", cmdChar, args[0]); cmd(args[0])
        #if len(args) == 2: cmd(args[0], args[1])

        if len(args) == 0: cmd()
        if len(args) == 1: cmd(args[0])
        if len(args) == 2: cmd(args[0], args[1])

    except:
      print("Noting + ignoring enoTurtle followPattern bug processing", command)
      traceback.print_exc()

################# exit on click #################

def exitonclick():     turtle.exitonclick()
def color(whichColor): global t; t.color(whichColor)
def pensize(size):     global t; t.pensize(size)
def speed(howFast):    global t; t.speed(howFast)

### end ###
