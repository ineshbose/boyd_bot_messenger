# flake8: noqa

import os
from flask import Blueprint, current_app

# def create_bot():
#     return Blueprint()

app_url = os.environ.get("APP_URL", "http://127.0.0.1:5000")

from . import _config

blueprint = Blueprint("boyd_bot", __name__, template_folder="templates")

webhook_token = os.environ.get("VERIFY_TOKEN")
wb_arg_name = os.environ.get("WB_ARG_NAME")


from .timetable import Timetable

timetable = Timetable()


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

if current_app.config["FEATURES"]["SCHEDULER"]:
    scheduler = Scheduler()
    scheduler.run()

from .bot import webhook, new_user_registration

blueprint.add_url_rule("/webhook", view_func=webhook, methods=["GET", "POST"])
blueprint.add_url_rule("/register/<reg_id>", view_func=new_user_registration, methods=["GET", "POST"])
