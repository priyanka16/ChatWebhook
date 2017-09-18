from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "This is just the start of the world"

if __name__ == '__main__':
    app.run()
