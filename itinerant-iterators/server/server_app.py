from find_bounds import find_bounds
from flask import Flask, request

app = Flask(__name__)


@app.get('/')
def home():
    """We can check if the site is up"""
    return "<p>Hello</p>"


@app.post("/")
def send_boxes():
    """Returns bounds"""
    return find_bounds(request.files['file'].read(), request.form["text"],
                       request.form["regex"] == "True")


app.run(host='0.0.0.0', port=81)
