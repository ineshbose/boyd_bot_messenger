import time
import atexit
from datetime import datetime, timedelta
from .. import db, timetable, platform
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    """
    Schedules certain jobs in the background.
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def clear_db(self):
        db.clear_db()

    def check_class(self):
        for data in db.get_all():
            time1 = datetime.now().isoformat()
            time2 = (datetime.now() + timedelta(minutes=10)).isoformat()
            if (
                data.get("subscribe")
                and timetable.login(data["_id"], data["uni_id"], data["uni_pw"])[0]
                and timetable.iterate(data["_id"], time1, time2)
            ):
                for msg in timetable.read(data["_id"], time1, time2):
                    msg = "Hey, {}! Hope you're on your way to\n{}".format(
                        platform.get_user_data(data["_id"]).get(
                                "first_name", "heads up"
                        ),
                        msg
                    )
                    platform.send_message(data["_id"], msg)

    def morning_alert(self):
        for data in db.get_all():
            if (
                data.get("subscribe")
                and timetable.login(data["_id"], data["uni_id"], data["uni_pw"])[0]
            ):
                for msg_no, msg in enumerate(
                    timetable.read(data["_id"], datetime.now().isoformat())
                ):
                    if msg_no == 0:
                        msg = "Morning, {}! Today is {} and your schedule is..\n{}".format(
                            platform.get_user_data(data["_id"]).get(
                                "first_name", "sunshine"
                            ),
                            datetime.now().strftime("%d %B (%A)"),
                            msg,
                        )
                    platform.send_message(data["_id"], msg)

    def run(self):
        self.scheduler.add_job(func=self.clear_db, trigger="interval", weeks=2)
        #self.scheduler.add_job(func=self.morning_alert, trigger="interval", seconds=10)
        self.scheduler.add_job(
            func=self.morning_alert,
            trigger="cron",
            month="09-11,1-3", # When university is on
            day_of_week="mon-fri", # Weekdays
            hour="08", # At 8AM every morning
        )
        self.scheduler.add_job(func=self.check_class, trigger="interval", minutes=10)
        self.scheduler.start()
