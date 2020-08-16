from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField
from wtforms import SubmitField, HiddenField, BooleanField


class RegisterForm(FlaskForm):
    reg_id = HiddenField("reg_id")
    uni_id = StringField("University ID", validators=[DataRequired()])
    uni_pw = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me", default=True)
    subscribe = BooleanField("Notify Me About My Schedule", default=False)
    submit = SubmitField("Login")
