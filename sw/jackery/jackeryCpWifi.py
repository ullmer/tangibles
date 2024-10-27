# CoPilot output 1/2 from query "please give python code for accessing current power level of jackery 1000 v2 via bluetooth or wifi"

import requests

def get_power_level():
    # Replace with your device's IP address and API endpoint
    url = "http://192.168.1.100/api/power_level"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('power_level')
    else:
        return None

power_level = get_power_level()
if power_level:
    print(f"Current power level: {power_level}")
else:
    print("Failed to retrieve power level")

