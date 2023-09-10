from find_bounds import find_bounds
from flask import Flask, request

app = Flask(__name__)


@app.get('/')
def home():
    """Just to show the site is working if we visit from browser"""
    return "<p>Hello</p>"


@app.post("/")
def send_boxes():
    """Returns the data from the function call"""
    return find_bounds(request.files['file'].read(), request.form["text"], request.form["regex"])


app.run(host='0.0.0.0', port=81)
