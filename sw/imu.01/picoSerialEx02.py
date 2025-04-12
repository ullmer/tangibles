#Code ~by CoPilot, 2025-04-12
# pip install pyserial

import serial, time
import serial.tools.list_ports

def find_pico_port():
  ports = serial.tools.list_ports.comports()
  for port in ports:
    print("port description: " + str(port.description))
    if "USB Serial Device" in port.description:  # Adjust this string based on your Pico's description
      return port.device
  return None

def send_command(ser, command):
  ser.write(b'\x03')  # Send Ctrl+C to interrupt any running code
  time.sleep(0.1)
  ser.write(b'\x01')  # Send Ctrl+A to enter raw REPL mode
  time.sleep(0.1)

  ser.write((command + '\n').encode('utf-8'))
  ser.flush()
  time.sleep(0.1) # Give some time for the command to be processed

  ser.write(b'\x04')  # Send Ctrl+D to execute the command
  ser.flush()
  time.sleep(0.1)

  response = ser.read_all().decode('utf-8')
  return response

def cli(ser):
  try:
    while True:
      command = input("Enter command for Pico: ")
      if command.lower() == "exit": break
      response = send_command(ser, command)
      print(f"Response: {response}")
  except KeyboardInterrupt:
    print("Exiting...")

def main():
  pico_port = find_pico_port()
  if pico_port is None:
    print("Raspberry Pi Pico not found.")
    return

  print(f"Raspberry Pi Pico found on port {pico_port}")

  # Establish serial communication
  ser = serial.Serial(pico_port, 115200, timeout=1)  # Adjust baud rate if necessary

  cpHeader = 'Adafruit CircuitPython'
  cpHLen   = len(cpHeader)

  try:
    ser.write(b'\n');         ser.flush()
    while True:
      if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Received: {line}")

        if line[0:cpHLen] == cpHeader: 
          print("!!!")
          time.sleep(0.1)
          ser.write("print(3)\n\n".encode('utf-8')); ser.flush()
          cli(ser)

        # You can send data to Pico using ser.write() method
        # ser.write(b'Your message here\n')
  except KeyboardInterrupt:
    print("Exiting...")
  finally:
    ser.close()

if __name__ == "__main__":
  main()

