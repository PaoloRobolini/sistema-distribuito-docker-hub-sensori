import socket
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    """Pagina principale - mostra l'hostname del container per verificare il load balancing."""
    hostname = socket.gethostname()
    return render_template("index.html", hostname=hostname)


@app.route("/publish", methods=["POST"])
def publish():
    # ============================================================
    # TODO FASE 2: Implementa la pubblicazione MQTT
    # ============================================================
    # 1. Ricevi il payload JSON dalla richiesta:
    #        data = request.get_json()
    #
    # 2. Importa paho.mqtt.client e crea un client MQTT:
    #        import paho.mqtt.client as mqtt
    #        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    #
    # 3. Connettiti al broker EMQX sulla rete interna Docker:
    #        client.connect("emqx", 1883, 60)
    #
    # 4. Pubblica il payload (come stringa JSON) sul topic "notifications":
    #        import json
    #        client.publish("notifications", json.dumps(data))
    #
    # 5. Disconnetti il client:
    #        client.disconnect()
    #
    # 6. Ritorna una risposta JSON di conferma:
    #        return jsonify({"status": "ok", "messaggio": "Dati pubblicati"})
    #
    # ============================================================
    return jsonify({"errore": "Rotta /publish non ancora implementata"}), 501


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
