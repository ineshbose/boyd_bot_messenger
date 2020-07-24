import os
import logging
from flask import Flask


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

app_url = os.environ.get("APP_URL", "http://127.0.0.1")
app.config["SECRET_KEY"] = os.environ["FLASK_KEY"]

from . import views
from . import _config
from .forms import RegisterForm

webhook_token = os.environ["VERIFY_TOKEN"]
wb_arg_name = os.environ["WB_ARG_NAME"]

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

platform = Platform(platform_token=os.environ["PLATFORM_TOKEN"])


def log(message):
    app.app.logger.info(message)
