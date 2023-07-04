import network
import time
import config

from umqtt.simple import MQTTClient
from machine import ADC, Pin

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
 
    print(wlan.isconnected())

    # Reconnect if it's necessary
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        print('waiting for connection...')
        time.sleep(1)
 
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed')
    else:
        print('connected')
        ip=wlan.ifconfig()[0]
        print('network config: ', ip)
        return ip

def connect_mqtt():
    client_id = config.CLINET_ID
    client = MQTTClient(client_id, "io.adafruit.com", user=config.ADAFRUIT_IO_USERNAME, password=config.ADAFRUIT_IO_KEY, port=1883)
    client.connect()
    return client

def publish_data(client, data):
    topic = "{}/feeds/{}".format(config.ADAFRUIT_IO_USERNAME, config.ADAFRUIT_IO_FEEDNAME)
    client.publish(topic, data)

# Ready 
connect_wifi()
client = connect_mqtt()

# Skapa en ADC-objekt
adc = ADC(Pin(26))

while True:
    # Read the analog value from the sensor
    value = adc.read_u16()
    
    #Print the value to check
    print("Gas level: ", value)
    
    # Convert data to string 
    publish_data(client, str(value))
    
    # Wait for a second before reading the value again
    time.sleep(5)






    



