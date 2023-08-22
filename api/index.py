from flask import Flask, render_template, Response
from werkzeug.exceptions import HTTPException
from boyd_bot import bot_blueprint

app = Flask(__name__)
app.register_blueprint(bot_blueprint(), url_prefix="/")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/robots.txt")
def robots():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.app_errorhandler(HTTPException)
def page_not_found(e):
    return render_template("error.html", error=e), e.code
