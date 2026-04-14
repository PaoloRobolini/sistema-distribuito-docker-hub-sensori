# ============================================================
# SMART CITY HUB - Worker MQTT Subscriber
# ============================================================
#
# TODO FASE 3: Implementa il Worker MQTT
#
# Questo microservizio deve:
#
# 1. Importare la libreria paho.mqtt.client
#        import paho.mqtt.client as mqtt
#
# 2. Definire la callback on_connect(client, userdata, flags, reason_code, properties):
#        - Stampare un messaggio di conferma connessione
#        - Sottoscriversi al topic "notifications"
#            client.subscribe("notifications")
#
# 3. Definire la callback on_message(client, userdata, message):
#        - Stampare il topic e il payload del messaggio ricevuto
#            print(f"[{message.topic}] {message.payload.decode()}")
#
# 4. Creare il client MQTT (ATTENZIONE alla versione 2.x!):
#        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#
# 5. Assegnare le callback:
#        client.on_connect = on_connect
#        client.on_message = on_message
#
# 6. Connettersi al broker EMQX sulla rete interna Docker:
#        client.connect("emqx", 1883, 60)
#
# 7. Avviare il loop di ascolto infinito:
#        client.loop_forever()
#
# ============================================================

print("Worker MQTT - Smart City Hub")
print("In attesa di implementazione...")
print("Completa questo file seguendo le istruzioni nei commenti sopra.")
