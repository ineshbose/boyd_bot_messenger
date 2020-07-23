from flask import render_template
from . import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
