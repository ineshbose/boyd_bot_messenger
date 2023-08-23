# flake8: noqa

import os
from flask import Blueprint
from boyd_bot.timetable import Timetable
from boyd_bot.bot import bot_functions
from boyd_bot import views
from boyd_bot.services import Guard, Database, Parser, Platform, Scheduler
from werkzeug.exceptions import HTTPException
from _config import config as default_config

def bot_blueprint(config=default_config):
    blueprint = Blueprint(
        "boyd_bot",
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/bb-static",
    )

    timetable = Timetable(config['TIMETABLE'])
    guard = Guard(key=os.environ.get("GUARD_KEY"))

    db = Database(
        db_token=os.environ.get("DB_MAIN_TOKEN"),
        key1=os.environ.get("DB_KEY1", "key1"),
        key2=os.environ.get("DB_KEY2", "key2"),
        guard=guard,
    )

    parser = Parser(db=db, timetable=timetable, config=config['PARSER'])
    platform = Platform(platform_token=os.environ.get("PLATFORM_TOKEN"))

    if False: # current_app.config["FEATURES"]["SCHEDULER"]:
        scheduler = Scheduler()
        scheduler.run()

    webhook, new_user_registration = bot_functions(
        config=config,
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

    if True:
        blueprint.add_url_rule("/", view_func=views.index)
        blueprint.add_url_rule("/terms", view_func=views.terms)
        blueprint.add_url_rule("/privacy", view_func=views.privacy)
        # blueprint.register_error_handler(HTTPException, f=views.page_not_found)

    return blueprint
