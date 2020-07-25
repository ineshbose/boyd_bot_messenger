from flask import render_template
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


@blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
