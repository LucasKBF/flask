from app import app
from flask import render_template
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    render_template("login.html")

