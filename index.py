from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hola mundo</h1>"

# def hello_world():
    # return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)