from flask import render_template, Response
from werkzeug.exceptions import HTTPException
from . import blueprint


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/privacy")
def privacy():
    return render_template("privacy.html")


@blueprint.route("/terms")
def terms():
    return render_template("terms.html")


@blueprint.route("/robots.txt")
def robots():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@blueprint.app_errorhandler(HTTPException)
def page_not_found(e):
    return render_template("error.html", error=e), e.code
