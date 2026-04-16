from flask import render_template, request, jsonify, Flask
import paho.mqtt.client as mqtt
import json
import socket

app = Flask(__name__)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

@app.route("/")
def index():
    """Pagina principale - mostra l'hostname del container per verificare il load balancing."""
    hostname = socket.gethostname()
    return render_template("index.html", hostname=hostname)

@app.route('/publish', methods=['POST'])
def publish():
    data = request.get_json()
    # print(f"Ricevuto dati: {data} e mi connetto al broker MQTT...")
    client.connect("emqx", 1883, 60)
    # Here you would typically publish the message to a message broker or perform some action
    # print(f"Pubblico dati: {data}")
    client.publish("notifications", json.dumps(data))
    client.disconnect()
    return jsonify({"status": "Message published", "data": data})

@app.route('/health', methods=['GET'])
def health():
    print("Controllo stato di salute dell'applicazione...")
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    # print("Flask app in esecuzione...")
    app.run(host='0.0.0.0', port=5000, debug=True)