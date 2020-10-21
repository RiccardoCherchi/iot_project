import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from RPLCD import CharLCD

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=10, pin_e=12, pins_data=[16, 15, 13, 11])

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print(client)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot/led")
    client.subscribe("test")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    json_message = None
    
    try:
        json_message = json.loads(msg.payload)
    except:
        print("json error")

    status = json_message['status']
    message = json_message['message']
    
    print(status)
    print(message)

    GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
    
    if status:   
        GPIO.output(8, GPIO.HIGH)
        lcd.write_string(u"%s" % (message))
    else:
        GPIO.output(8, GPIO.LOW)
        lcd.clear()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.101", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
