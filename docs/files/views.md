# [`views.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/views.py)

All simple views are rendered using `render_template()`.


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
    submit = SubmitField("Login")
```



## `views`

```python
@app.route("/")
def index():
    """
    Returns index() view for the app.
    """
    return render_template("index.html")



@pages.route("/privacy")
def privacy():
    """
    Returns privacy() view for the app.
    """
    return render_template("privacy.html")


@pages.route("/terms")
def terms():
    """
    Returns terms() view for the app.
    """
    return render_template("terms.html")


@pages.app_errorhandler(404)
def page_not_found(e):
    """
    Handles 404 error for the app.
    """
    return render_template("404.html"), 404

```