# [`Views & Templates`](#)

This script contains all simple views for the app and are linked using `Blueprint`.



## [`views.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/views.py)

All simple views are rendered using `render_template()`.


### Packages Used

* [flask_wtf](https://github.com/lepture/flask-wtf)
* [wtforms](https://github.com/wtforms/wtforms)



### `RegisterForm`

`FlaskForm` with necessary details to register a user.

```python
class RegisterForm(FlaskForm):
    uid = HiddenField("uid")
    uni_id = StringField("University ID", validators=[DataRequired()])
    uni_pass = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
```



### `views`

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



## [templates](https://github.com/ineshbose/boyd_bot_messenger/blob/master/templates)

### `register.html`

This is the registration form. Tailor this according to your university.

```html
<!-- It's a good idea to style the registration form with a theme that is familiar to users and can get their trust.-->
```


### Rest of the Templates

The theme used is [Grayscale from Start Bootstrap](https://startbootstrap.com/themes/grayscale/).