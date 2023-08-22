# flake8: noqa

import os
from flask import Blueprint
from timetable import Timetable
from bot import bot_functions
from services import Guard, Database, Parser, Platform, Scheduler

def bot_blueprint():
    blueprint = Blueprint("boyd_bot", __name__, template_folder="templates")

    timetable = Timetable()
    guard = Guard(key=os.environ.get("GUARD_KEY"))

    db = Database(
        db_token=os.environ.get("DB_MAIN_TOKEN"),
        key1=os.environ.get("DB_KEY1", "key1"),
        key2=os.environ.get("DB_KEY2", "key2"),
        guard=guard,
    )

    parser = Parser(db=db, timetable=timetable)
    platform = Platform(platform_token=os.environ.get("PLATFORM_TOKEN"))

    if False: # current_app.config["FEATURES"]["SCHEDULER"]:
        scheduler = Scheduler()
        scheduler.run()

    webhook, new_user_registration = bot_functions(
        {},
        webhook_token=os.environ.get("VERIFY_TOKEN"),
        wb_arg_name=os.environ.get("WB_ARG_NAME"),
        timetable=timetable,
        guard=guard,
        db=db,
        parser=parser,
        platform=platform,
    )

    blueprint.add_url_rule("/webhook", view_func=webhook, methods=["GET", "POST"])
    blueprint.add_url_rule("/register/<reg_id>", view_func=new_user_registration, methods=["GET", "POST"])

    return blueprint
