import json

import paho.mqtt.client as mqtt

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print(client)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test")
    client.subscribe("iot/light")


client.on_connect = on_connect

client.connect("127.0.0.1", 1883, 60)


send = True
while send:
    message = input("press enter to light the led ")
    if message is not None:
        client.publish("iot/light", payload=json.dumps({"status": True}))
    send_input = input("send another input? Y/n -> ")
    if send_input != 'Y' and send_input != 'y':
        send = False
        break
