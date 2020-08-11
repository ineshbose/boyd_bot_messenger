# [`forms.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/forms.py)


## Packages Used

* [flask_wtf](https://github.com/lepture/flask-wtf)
* [wtforms](https://github.com/wtforms/wtforms)



## `RegisterForm`

`FlaskForm` with necessary details to register a user.

```python
class RegisterForm(FlaskForm):
    reg_id = HiddenField("reg_id")
    uni_id = StringField("University ID", validators=[DataRequired()])
    uni_pw = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Login")
```
