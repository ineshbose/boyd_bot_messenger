import time
import atexit
import datetime
from .. import db, timetable, platform, app
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler


class Scheduler:
    """
    Schedules certain jobs in the background.
    """

    def __init__(self):
        if app.config["FEATURES"]["SCHEDULER"]["APP"]:
            self.scheduler = BackgroundScheduler()
        elif app.config["FEATURES"]["SCHEDULER"]["SERVER"]:
            self.scheduler = BlockingScheduler()

    def clear_db(self):
        db.clear_db()

    def remind(self):
        dataset = db.get_list()
        for data in dataset:
            if data.get("subscribe"):
                if timetable.login(data["_id"], data["uni_id"], data["uni_pw"])[0]:
                    res = timetable.read(
                        data["_id"], datetime.datetime.now().isoformat()
                    )
                    for r in res:
                        platform.send_message(data["_id"], r)

    def run(self):
        self.scheduler.add_job(func=self.clear_db, trigger="interval", weeks=2)
        # self.scheduler.add_job(func=self.remind, trigger="interval", seconds=10)
        self.scheduler.add_job(func=self.remind, trigger="cron", day_of_week="0-4", hour="08")
        self.scheduler.start()
