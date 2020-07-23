# [`views.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/views.py)

All simple views are rendered using `render_template()`.



```python
@app.route("/")
def index():
    """
    Returns index() view for the app.
    """
    return render_template("index.html")



@app.route("/privacy")
def privacy():
    """
    Returns privacy() view for the app.
    """
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    """
    Returns terms() view for the app.
    """
    return render_template("terms.html")


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 error for the app.
    """
    return render_template("404.html"), 404

```