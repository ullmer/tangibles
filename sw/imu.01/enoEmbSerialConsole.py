# Serial interactions with circuitpython embedded devices
# Brygg Ullmer, Clemson University 
# pip install pyserial

import serial, time
import serial.tools.list_ports

class enoEmbSerialConsole:

  ################## constructor ##################

  def __init__(self): 
    self.initConsole()

  ################## find embedded-device serial port ##################
  
  def find_embedded_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
      print("port description: " + str(port.description))
      if "USB Serial Device" in port.description:  # Adjust this string based on your Pico's description
        return port.device
    return None
  
  ################## send interrupt-and-clear to circuitpython device ##################
  
  def interruptAndClear(ser):
    ser.write(b'\x03'); time.sleep(0.1) # Send Ctrl+C to interrupt any running code
    ser.write(b'\x01'); time.sleep(0.1) # Send Ctrl+A to enter raw REPL mode
  
  ################## send command to circuitpython device ##################
  
  def sendCommand(ser, command):
    interruptAndClear(ser)
    ser.write((command + '\n').encode('utf-8')); ser.flush(); time.sleep(0.1) 
    ser.write(b'\x04'); ser.flush(); time.sleep(0.1) # Send Ctrl+D to execute the command
  
    response  = ser.read_all().decode('utf-8')
    response2 = response[29:-4] #clear prefix (some interrupt&clear-based) and postfix
    return response2
  
  ################## command-line interface to serial-linked embedded device ##################
  
  def cli(ser):
    try:
      while True:
        command = input("Enter command for Pico: ")
        if command.lower() == "exit": break
        response = sendCommand(ser, command)
        print(f">> {response}")
  
    except KeyboardInterrupt:
      print("Exiting...")
  
  ################## main ##################
  
  def initConsole():
    pico_port = find_embedded_port()
    if pico_port is None:
      print("CircuitPython device not found."); return
  
    print(f"CircuitPython device found on port {pico_port}")
  
    ser = serial.Serial(pico_port, 115200, timeout=1); # Establish serial communication
  
    cpHeader = 'Adafruit CircuitPython'
    cpHLen   = len(cpHeader)
  
    try:
      interruptAndClear(ser); time.sleep(.1)
      cmd = b'\n'; ser.write(cmd); ser.flush(); time.sleep(.1)
      cmd = "from enoEmbBase import *\n".encode('utf-8') + b'\x04'
      ser.write(cmd); ser.flush(); time.sleep(.1)
  
      while True:
        if ser.in_waiting > 0:
          line = ser.readline().decode('utf-8').rstrip()
          print(f"Received: {line}")
          interruptAndClear(ser)
  
          if line[0:cpHLen] == cpHeader: 
            print("connection established")
            time.sleep(0.1)
            cli(ser)
  
    except KeyboardInterrupt:
      print("exiting...")
    finally:
      ser.close()
  
  if __name__ == "__main__":
    eesc = enoEmbSerialConsole()
  
  ### end ###
