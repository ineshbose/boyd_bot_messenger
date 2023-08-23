from flask import render_template

def index():
    return render_template("index.html")

def privacy():
    return render_template("privacy.html")

def terms():
    return render_template("terms.html")

def page_not_found(e):
    return render_template("error.html", error=e), e.code