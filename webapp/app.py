import socket
import json
from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)


@app.route("/")
def index():
    """Pagina principale - mostra l'hostname del container per verificare il load balancing."""
    hostname = socket.gethostname()
    return render_template("index.html", hostname=hostname)


@app.route("/publish", methods=["POST"])
def publish():
    """Riceve un payload JSON e lo pubblica sul topic MQTT 'notifications'."""
    data = request.get_json()

    if not data:
        return jsonify({"errore": "Payload JSON mancante"}), 400

    # Crea un client MQTT (versione 2.x) e pubblica il messaggio
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect("emqx", 1883, 60)
    client.publish("notifications", json.dumps(data))
    client.disconnect()

    return jsonify({"status": "ok", "messaggio": "Dati pubblicati su MQTT", "dati": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
