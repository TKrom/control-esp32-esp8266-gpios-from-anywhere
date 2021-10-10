#Micropython implementation of the code of Rui Santos; complete project details at https://RandomNerdTutorials.com/control-esp32-esp8266-gpios-from-anywhere/
"""
From here on the code is placed in the main.py file.
"""

def http_get_request(server_name):
    _, _, host, path = server_name.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    try:
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    except:
        payload = "SocketError"
        return payload
    while True:
        data = s.recv(100)
        if data:
            #print("data type:", type(data))
            #print(str(data, 'utf8'))
            payload = str(data, 'utf8')
            #print("data_string is:", payload)
        else:
            break
    payload = payload[43:] #Removing the first 43 characters of the resulting string, the rest contains the payload.
    try:
        payload = json.loads(payload)
        return payload
        s.close()
    except:
        payload = "PayloadError"
        return payload

def main_function():
    current_millis = time.ticks_ms()
    global previous_millis
    global interval
    global server_name
    if (current_millis - previous_millis >= interval):
        #Check Wifi status.
        if sta_if.isconnected():
            outputs_state = http_get_request(server_name)
            if (outputs_state != "PayloadError") & (outputs_state != "SocketError"):
                print(outputs_state)
                my_object = outputs_state
                if type(my_object) != dict:
                    print("Parsing input failed!")
                    return
                keys = list(my_object)
                gpio_pins = []
                for index, key in enumerate(keys):
                    #gpio_pins.append(Pin(int(key), Pin.OUT))
                    value = my_object[key]
                    print("GPIO: ", key, "SET to: ", value)
                    #gpio_pins[index].value(value) #Set the correct GPIO pin to the desired value.
                    temp_pin = Pin(int(key), Pin.OUT)
                    temp_pin.value(int(value))
                previous_millis = current_millis
            else:
                if outputs_state == "PayloadError":
                    print("PayloadError")
                elif outputs_state == "SocketError":
                    print("SocketError")
                pass
        else:
            print("WiFi disconnected!")

while True:
    main_function()