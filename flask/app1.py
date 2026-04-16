import flask

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return 'Ciao da app 1!'

if __name__ == '__main__':
    app.run(debug=True, port=5000)