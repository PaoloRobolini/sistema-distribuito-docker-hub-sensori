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
    client.connect("emqx", 1883, 60)
    # Here you would typically publish the message to a message broker or perform some action
    print(f"Pubblico dati: {data}")
    client.publish("topic", json.dumps(data))
    client.disconnect()
    return jsonify({"status": "Message published", "data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)