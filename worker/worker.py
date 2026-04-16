import paho.mqtt.client as mqtt

BROKER_HOST = "emqx"
BROKER_PORT = 1883
TOPIC = "notifications"


def on_connect(client, userdata, flags, reason_code, properties):
    """Callback alla connessione: sottoscrizione al topic."""
    if reason_code == 0:
        print(f"Connesso al broker MQTT ({BROKER_HOST}:{BROKER_PORT})")
        client.subscribe(TOPIC)
        print(f"Sottoscritto al topic '{TOPIC}' - in attesa di messaggi...")
    else:
        print(f"Connessione fallita con codice: {reason_code}")


def on_message(client, userdata, message):
    """Callback alla ricezione di un messaggio: stampa il contenuto."""
    payload = message.payload.decode()
    print(f"[{message.topic}] Messaggio ricevuto: {payload}")


if __name__ == "__main__":
    print("Worker MQTT - Smart City Hub")
    print(f"Connessione al broker {BROKER_HOST}:{BROKER_PORT}...")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()
