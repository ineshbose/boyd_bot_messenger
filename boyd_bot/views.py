from flask import render_template
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


@blueprint.app_errorhandler(HTTPException)
def page_not_found(e):
    return render_template("error.html", error=e), e.code
