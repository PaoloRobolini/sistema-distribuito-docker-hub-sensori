import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connesso al broker MQTT!")
    client.subscribe("notifications")

def on_message(client, userdata, message):
    print(f"Messaggio ricevuto su {message.topic}: {message.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
print("Connettendo al broker MQTT...")
client.connect("emqx", 1883, 60)
client.loop_forever()