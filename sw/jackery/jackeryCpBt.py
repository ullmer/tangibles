# CoPilot output 2/2 from query "please give python code for accessing current power level of jackery 1000 v2 via bluetooth or wifi"

import bluetooth

def get_power_level():
    # Replace with your device's Bluetooth address
    bd_addr = "XX:XX:XX:XX:XX:XX"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    # Send a command to get power level (this command depends on the device's protocol)
    sock.send("GET_POWER_LEVEL")

    # Receive the response
    data = sock.recv(1024)
    sock.close()

    return data.decode('utf-8')

power_level = get_power_level()
print(f"Current power level: {power_level}")

