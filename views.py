from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField, HiddenField


pages = Blueprint("pages", __name__, template_folder="templates")


class RegisterForm(FlaskForm):
    uid = HiddenField("uid")
    uni_id = StringField("University ID", validators=[DataRequired()])
    uni_pass = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@pages.route("/")
def index():
    return render_template("index.html")


@pages.route("/privacy")
def privacy():
    return render_template("privacy.html")


@pages.route("/terms")
def terms():
    return render_template("terms.html")


@pages.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
