import os
import logging
import threading
from flask import Flask, Blueprint


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

app_url = os.environ.get("APP_URL", "http://127.0.0.1")
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")

from . import _config

blueprint = Blueprint("boyd_bot", __name__, template_folder="templates")

from . import views
from .forms import *

webhook_token = os.environ.get("VERIFY_TOKEN")
wb_arg_name = os.environ.get("WB_ARG_NAME")


from .timetable import Timetable

timetable = Timetable(
    "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"
)


from .services.guard import Guard

guard = Guard(key=os.environ.get("GUARD_KEY"))


from .services.database import Database

db = Database(
    db_token=os.environ.get("DB_MAIN_TOKEN"),
    key1=os.environ.get("DB_KEY1", "key1"),
    key2=os.environ.get("DB_KEY2", "key2"),
)


from .services.parser import Parser

parser = Parser()


from .services.platform import Platform

platform = Platform(platform_token=os.environ.get("PLATFORM_TOKEN"))


from .services.scheduler import Scheduler

if (app.config["FEATURES"]["SCHEDULER"]["APP"]
    and not app.config["FEATURES"]["SCHEDULER"]["SERVER"]):
    scheduler = Scheduler()
    scheduler.run()


def log(message):
    app.logger.info(message)


from .app import *

app.register_blueprint(blueprint, url_prefix=app.config["URL_ROOT"])


@app.after_request
def secure_http_header(response):
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src * 'unsafe-inline'"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Feature-Policy"] = "none"
    return response
