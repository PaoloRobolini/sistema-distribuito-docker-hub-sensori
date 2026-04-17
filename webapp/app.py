from flask import Flask, jsonify, render_template, request
import socket

app = Flask(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    return render_template("index.html", hostname=hostname)

app.run(
    '0.0.0.0', 5000
)