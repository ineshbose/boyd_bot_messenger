import time
import atexit
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from .. import db, timetable, platform


def clear_db():
    db.clear_db()

def remind():
    dataset = db.get_list()
    for data in dataset:
        if data.get("uni_id"):
            if timetable.login(data["_id"], data["uni_id"], data["uni_pw"])[0]:
                res = timetable.read(data["_id"], datetime.datetime.now().isoformat())
                for r in res:
                    platform.send_message(data["_id"], r)

scheduler = BackgroundScheduler()
scheduler.add_job(func=clear_db, trigger="interval", weeks=2)
scheduler.add_job(func=remind, trigger="cron", hour="08")
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())