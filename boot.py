#Micropython implementation of the code of Rui Santos; complete project details at https://RandomNerdTutorials.com/control-esp32-esp8266-gpios-from-anywhere/
"""
This part should be included in the boot.py file.
"""

import network
import time
import socket
import json
from machine import Pin



###########################################################################################################


#ACTION REQUIRED: PLEASE FILL IN THE WIFI INFORMATION BELOW.
ssid = "REPLACE_WITH_YOUR_SSID"
password = "REPLACE_WITH_YOUR_PASSWORD"

#Your IP address or domain name with URL path
server_name = "http://example.com/esp-outputs-action.php?action=outputs_state&board=1"

#Update interval time set to 5 seconds
interval = 5000
previous_millis = 0


###########################################################################################################

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True) #Only put the EPS32 in station mode, not in access point mode.
ap_if.active(False)

#Connect to the WiFi router as requested.
sta_if.connect(ssid, password)
print("Connecting")
while not sta_if.isconnected():
    time.sleep(0.5)
    print(".")
print("")
print("Connected to WiFi network with IP Address, netmask, gateway, DNS: ")
ap_if.ifconfig()
