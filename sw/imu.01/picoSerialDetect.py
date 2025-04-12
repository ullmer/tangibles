#Code ~by CoPilot, 2025-04-12
# pip install pyserial

import serial
import serial.tools.list_ports

def find_pico_port():
  ports = serial.tools.list_ports.comports()
  for port in ports:
    print("port description: " + str(port.description))
    if "USB Serial Device" in port.description:  # Adjust this string based on your Pico's description
      return port.device
  return None

def main():
  pico_port = find_pico_port()
  if pico_port is None:
    print("Raspberry Pi Pico not found.")
    return

  print(f"Raspberry Pi Pico found on port {pico_port}")

  # Establish serial communication
  ser = serial.Serial(pico_port, 115200)  # Adjust baud rate if necessary

  try:
    while True:
      if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Received: {line}")
        # You can send data to Pico using ser.write() method
        # ser.write(b'Your message here\n')
  except KeyboardInterrupt:
    print("Exiting...")
  finally:
    ser.close()

if __name__ == "__main__":
  main()

